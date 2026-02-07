import uuid
import time
import redis
import json
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from app.core.celery_app import celery_app
from app.core.config import settings
from app.models.search import SearchRequest, SearchStatus
from app.models.contract import ContractResult, MatchType, SpecComparisonRow, MatchStatus
from app.services.zakupki_parser import ZakupkiSearcher as ParserZakupkiSearcher
from app.services.zakupki_searcher import ZakupkiSearcher as DetailZakupkiSearcher
from app.services.llm_engine import llm_engine
from app.services.matcher import calculate_match_score


def get_db_session():
    """Create a database session"""
    engine = create_engine(settings.DB_URL)
    return Session(engine)


def get_redis_client():
    """Create a Redis client"""
    return redis.Redis.from_url(settings.REDIS_URL)


def _execute_search_task_logic(task_self, search_id: uuid.UUID):
    """
    Core logic for execute_search_task, separated for testing.
    
    Args:
        task_self: The Celery task instance (for update_state calls)
        search_id: UUID of the search request
    """
    redis_client = get_redis_client()
    stop_signal_key = f"stop_signal:{search_id}"
    
    db = None  # Initialize db to None
    try:
        # Get database session
        db = get_db_session()
        
        # Fetch search request from database
        search_request = db.query(SearchRequest).filter(SearchRequest.id == search_id).first()
        
        if not search_request:
            task_self.update_state(state='FAILURE', meta={'error': f'Search request {search_id} not found'})
            return {'status': 'error', 'message': f'Search request {search_id} not found'}
        
        # Update status to RUNNING (using the new status)
        search_request.status = SearchStatus.RUNNING
        search_request.processing_started_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.commit()
        
        # Step 1: Call ZakupkiSearcher.search() -> Get List
        task_self.update_state(
            state='PROGRESS',
            meta={'current': 0, 'total': 100, 'progress': 0.0, 'message': 'Starting search...'}
        )
        
        # Parse date strings if provided
        date_from = None
        date_to = None
        if search_request.date_from:
            date_from = datetime.strptime(search_request.date_from, "%Y-%m-%d").date()
        if search_request.date_to:
            date_to = datetime.strptime(search_request.date_to, "%Y-%m-%d").date()
        
        # Calculate max_pages dynamically based on limit_contracts (50 contracts per page)
        import math
        max_pages = math.ceil(search_request.limit_contracts / 50)
        
        # Create parser searcher and search for contracts
        parser_searcher = ParserZakupkiSearcher()
        search_result = parser_searcher.search(
            fz_44=True,
            region=search_request.region_filter,
            ktru=search_request.ktru_code,
            date_from=date_from,
            date_to=date_to,
            max_pages=max_pages
        )
        
        # Update total contracts found
        search_request.total_contracts_found = len(search_result.cards)
        db.commit()
        
        # Step 2: Loop through list (up to limit)
        contracts_to_process = search_result.cards[:search_request.limit_contracts]
        total_to_process = len(contracts_to_process)
        
        if total_to_process == 0:
            search_request.status = SearchStatus.COMPLETED
            search_request.processing_completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            db.commit()
            return {
                'status': 'completed',
                'message': f'Search {search_id} completed - no contracts found',
                'search_id': str(search_id)
            }
        
        # Create detail searcher for fetching contract details
        detail_searcher = DetailZakupkiSearcher(search_id)
        
        # Check for stop signal before starting processing
        if redis_client.exists(stop_signal_key):
            # Stop signal detected - update status to CANCELLED
            search_request.status = SearchStatus.CANCELLED
            db.commit()

            # Clear the stop signal
            redis_client.delete(stop_signal_key)

            return {
                'status': 'cancelled',
                'message': f'Search {search_id} cancelled by stop signal before processing',
                'progress': 0,
                'processed': 0
            }
        
        # Extract user's technical specification for comparison
        user_technical_spec = search_request.technical_specification
        
        processed_count = 0
        for i, contract_card in enumerate(contracts_to_process):
            # Step 3: Check Stop Signal
            if redis_client.exists(stop_signal_key):
                # Stop signal detected - update status to STOPPED (using the new status)
                search_request.status = SearchStatus.STOPPED
                db.commit()
                
                # Clear the stop signal
                redis_client.delete(stop_signal_key)
                
                return {
                    'status': 'stopped',
                    'message': f'Search {search_id} stopped by user',
                    'progress': i / total_to_process,
                    'processed': i
                }
            
            # Update progress
            progress = (i + 1) / total_to_process
            task_self.update_state(
                state='PROGRESS',
                meta={
                    'current': i + 1,
                    'total': total_to_process,
                    'progress': progress,
                    'message': f'Processing contract {i+1}/{total_to_process}: {contract_card.reestr_number}'
                }
            )
            
            try:
                # Step 4: Call ZakupkiSearcher.get_details() -> llm_engine.extract -> matcher.compare
                contract_details = detail_searcher.parse_contract_details(
                    contract_card.reestr_number,
                    search_request.ktru_code
                )
                
                if not contract_details.get('success'):
                    # Skip failed contracts
                    continue
                
                # Extract specification text from objects
                spec_text = None
                if contract_details.get('objects') and contract_details['objects'].get('specification_text'):
                    spec_text = contract_details['objects']['specification_text']
                
                # If no spec text in objects, check attachments
                if not spec_text and contract_details.get('attachments'):
                    # In a real implementation, we would parse attachments
                    # For now, we'll use a placeholder
                    spec_text = f"Contract {contract_card.reestr_number} details"
                
                # Use LLM to extract specifications from contract
                contract_extracted_specs = {}
                if spec_text:
                    try:
                        contract_extracted_specs = llm_engine.extract_specs(
                            spec_text,
                            search_request.ktru_code
                        )
                    except Exception as e:
                        # Log LLM extraction error but continue
                        print(f"LLM extraction error for {contract_card.reestr_number}: {e}")
                
                # Use LLM to extract specifications from user's technical specification
                user_extracted_specs = {}
                if user_technical_spec:
                    try:
                        user_extracted_specs = llm_engine.extract_specs(
                            user_technical_spec,
                            search_request.ktru_code
                        )
                    except Exception as e:
                        # Log LLM extraction error but continue
                        print(f"LLM extraction error for user specs: {e}")
                
                # Compare user specs with contract specs
                ai_score = 0.0
                match_type = MatchType.NO_MATCH
                
<<<<<<< HEAD
                if extracted_specs:
                    # Placeholder for target specs
                    target_specs = {
                        "product_name": search_request.ktru_code,
                        "technical_specs": {}
                    }
                    
                    try:
                        comparison_result = llm_engine.compare_specs(target_specs, extracted_specs)
                        ai_score = comparison_result.get('overall_match_score', 0.0) * 100
                        
                        if ai_score >= 90:
                            match_type = MatchType.EXACT
                        elif ai_score >= 70:
                            match_type = MatchType.PARTIAL
                        elif ai_score >= 50:
                            match_type = MatchType.SIMILAR
                            
                    except Exception as e:
                        print(f"LLM comparison error for {contract_card.reestr_number}: {e}")
=======
                if contract_extracted_specs and user_extracted_specs:
                    # Calculate match score using the matcher
                    try:
                        # Get technical specs from both
                        contract_specs = contract_extracted_specs.get('technical_specs', {})
                        user_specs = user_extracted_specs.get('technical_specs', {})
                        
                        # Calculate overall match score
                        total_score = 0.0
                        matched_specs = 0
                        
                        for key, user_value in user_specs.items():
                            if key in contract_specs:
                                contract_value = contract_specs[key]
                                # Calculate match score for this specification
                                score = calculate_match_score(str(user_value), str(contract_value))
                                total_score += score
                                matched_specs += 1
                        
                        if matched_specs > 0:
                            ai_score = total_score / matched_specs
                            
                            # Determine match type based on score
                            if ai_score >= 90:
                                match_type = MatchType.EXACT
                            elif ai_score >= 70:
                                match_type = MatchType.PARTIAL
                            elif ai_score >= 50:
                                match_type = MatchType.SIMILAR
                            else:
                                match_type = MatchType.NO_MATCH
                    except Exception as e:
                        print(f"Error calculating match score for {contract_card.reestr_number}: {e}")
>>>>>>> 7c5e00a77cfb12ace2395c0342959a4e695731f6
                
                # Step 5: Save ContractResult to DB
                contract_result = ContractResult(
                    search_id=search_id,
                    reestr_number=contract_card.reestr_number,
                    contract_number=contract_card.reestr_number,  # Using reestr number as contract number
                    contract_date=contract_card.contract_date.strftime("%Y-%m-%d") if contract_card.contract_date else None,
                    match_type=match_type,
                    ai_score=ai_score,
                    confidence_level=search_request.confidence_threshold,
                    supplier_name=None,  # Would be extracted from contract_details in real implementation
                    customer_name=None,  # Would be extracted from contract_details in real implementation
                    contract_price=contract_card.price,
                    currency="RUB",
                    source_system="zakupki.gov.ru",
                    source_url=contract_card.link,
                    scraped_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    raw_data_json=json.dumps(contract_details) if contract_details else None
                )
                
                db.add(contract_result)
                db.flush()  # Get the ID for foreign key
                
                # Create spec comparison rows if we have both contract and user specs
                if contract_extracted_specs and user_extracted_specs:
                    contract_specs = contract_extracted_specs.get('technical_specs', {})
                    user_specs = user_extracted_specs.get('technical_specs', {})
                    
                    for key, user_value in user_specs.items():
                        if key in contract_specs:
                            contract_value = contract_specs[key]
                            # Calculate match score for this specification
                            similarity_score = calculate_match_score(str(user_value), str(contract_value))
                            
                            # Determine match status
                            match_status = MatchStatus.NO_MATCH
                            if similarity_score >= 90:
                                match_status = MatchStatus.EXACT_MATCH
                            elif similarity_score >= 70:
                                match_status = MatchStatus.PARTIAL_MATCH
                            elif similarity_score >= 50:
                                match_status = MatchStatus.SIMILAR
                            
                            spec_row = SpecComparisonRow(
                                contract_result_id=contract_result.id,
                                name=key,
                                target_value=str(user_value),
                                actual_value=str(contract_value),
                                match_status=match_status,
                                similarity_score=similarity_score
                            )
                            db.add(spec_row)
                
                # Step 6: Emit SSE event (processed + 1)
                search_request.contracts_processed += 1
                db.commit()
                
                processed_count += 1
                
                # Small delay to avoid overwhelming the system
                time.sleep(0.1)
                
            except Exception as e:
                # Log error but continue with next contract
                print(f"Error processing contract {contract_card.reestr_number}: {e}")
                db.rollback()
                continue
        
        # Step 7: Finalize: Update Status -> DONE. Save global stats.
        search_request.status = SearchStatus.COMPLETED
        search_request.processing_completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.commit()
        
        # Clean up
        detail_searcher.close()
        
        return {
            'status': 'completed',
            'message': f'Search {search_id} completed successfully. Processed {processed_count}/{total_to_process} contracts.',
            'search_id': str(search_id),
            'processed': processed_count,
            'total': total_to_process
        }
        
    except SQLAlchemyError as e:
        # Database error
        task_self.update_state(state='FAILURE', meta={'error': str(e)})
        return {'status': 'error', 'message': f'Database error: {str(e)}'}
        
    except Exception as e:
        # General error
        task_self.update_state(state='FAILURE', meta={'error': str(e)})
        return {'status': 'error', 'message': f'Unexpected error: {str(e)}'}
    
    finally:
        # Ensure the database session is closed
        if db:
            db.close()


@celery_app.task
def example_task(message: str):
    """Example Celery task"""
    return f"Task completed: {message}"


@celery_app.task(bind=True)
def execute_search_task(self, search_id: uuid.UUID):
    """
    Execute search task with state management and stop signal support.
    
    Args:
        search_id: UUID of the search request
    """
    return _execute_search_task_logic(self, search_id)