"""
Orchestration Service for Service Alpha.

This module orchestrates the end-to-end workflow:
1. Search contracts using scraper
2. Parse contract details
3. Extract document content
4. Process with AI for specification extraction and comparison
5. Normalize and match specifications
6. Calculate NMC values
7. Store results in database
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from decimal import Decimal

from app.services.scraper.searcher import ZakupkiSearcher, SearchParams, SearchResult
from app.services.scraper.parser import ContractParser
from app.services.docs.extractor import DocumentExtractor
from app.services.ai.prompts import (
    extract_specs_from_tz,
    extract_specs_from_contract,
    compare_specs
)
from app.services.matcher.normalizer import normalize_specification
from app.services.calc import calculate_nmc
from app.services.redis_service import (
    publish_search_progress,
    publish_search_status,
    publish_search_error
)
from app.models import SearchStatus, SearchRequest, ContractResult, SpecComparisonRow, MatchType
from app.database import SyncSessionLocal

logger = logging.getLogger(__name__)


def run_async(coro):
    """Run async coroutine in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)


class OrchestrationService:
    """Orchestrates the end-to-end contract search and analysis workflow."""
    
    def __init__(self, search_id: str, db_session):
        """
        Initialize orchestrator for a specific search.
        
        Args:
            search_id: Search request ID
            db_session: Database session
        """
        self.search_id = search_id
        self.db = db_session
        self.searcher = ZakupkiSearcher()
        self.parser = ContractParser()
        self.extractor = DocumentExtractor()
        
        # Load search request
        self.search_request = self.db.query(SearchRequest).filter(
            SearchRequest.id == search_id
        ).first()
        
        if not self.search_request:
            raise ValueError(f"Search request {search_id} not found")
    
    def check_stop_signal(self) -> bool:
        """Check if search should be stopped."""
        # Refresh search request from database
        self.db.refresh(self.search_request)
        return self.search_request.status == SearchStatus.STOPPED
    
    def update_progress(self, processed_count: int, message: str = ""):
        """Update search progress in database."""
        try:
            self.search_request.processed_count = processed_count
            if message:
                logger.info(f"Search {self.search_id}: {message}")
            self.db.commit()
        except Exception as e:
            logger.error(f"Failed to update progress: {e}")
            self.db.rollback()
    
    def process_contract(self, contract_info: Dict[str, Any], tz_specs: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """
        Process a single contract through the entire pipeline.
        
        Args:
            contract_info: Contract information from scraper
            tz_specs: Target specifications from TZ
            
        Returns:
            Processed contract result or None if processing failed
        """
        try:
            reestr_number = contract_info.get("reestr_number")
            contract_url = contract_info.get("link")
            
            if not reestr_number or not contract_url:
                logger.warning(f"Skipping contract without reestr number or URL: {contract_info}")
                return None
            
            logger.info(f"Processing contract {reestr_number}")
            
            # Step 1: Parse contract details
            contract_details = self.parser.parse_card(contract_url)
            if not contract_details:
                logger.warning(f"Failed to parse contract {reestr_number}")
                return None
            
            # Step 2: Extract document content if available
            document_text = ""
            if contract_details.get("attachments"):
                # Try to extract text from first attachment
                for attachment in contract_details.get("attachments", [])[:1]:  # Limit to first attachment
                    try:
                        doc_text = self.extractor.extract_text(attachment.get("url", ""))
                        if doc_text:
                            document_text = doc_text
                            break
                    except Exception as e:
                        logger.warning(f"Failed to extract document text: {e}")
            
            # Step 3: Extract specifications from contract using AI
            contract_specs = []
            if document_text:
                try:
                    contract_specs = extract_specs_from_contract(document_text)
                except Exception as e:
                    logger.warning(f"Failed to extract specs from contract: {e}")
            
            # Step 4: Compare specifications using AI
            comparison_result = None
            if tz_specs and contract_specs:
                try:
                    comparison_result = compare_specs(tz_specs, contract_specs)
                except Exception as e:
                    logger.warning(f"Failed to compare specs: {e}")
            
            # Step 5: Determine match type and score
            match_type = MatchType.NO_MATCH
            ai_score = 0
            
            if comparison_result:
                ai_score = comparison_result.get("score", 0)
                match_type_str = comparison_result.get("match_type", "NO_MATCH")
                
                # Map string to enum
                if match_type_str == "IDENTICAL":
                    match_type = MatchType.IDENTICAL
                elif match_type_str == "HOMOGENEOUS":
                    match_type = MatchType.HOMOGENEOUS
                elif match_type_str == "PARTIAL":
                    match_type = MatchType.PARTIAL
                else:
                    match_type = MatchType.NO_MATCH
            
            # Step 6: Prepare result
            result = {
                "reestr_number": reestr_number,
                "contract_url": contract_url,
                "sign_date": contract_details.get("sign_date"),
                "unit_price": contract_details.get("unit_price"),
                "match_type": match_type,
                "ai_score": ai_score,
                "manufacturer_target": None,  # Would come from TZ
                "manufacturer_found": contract_details.get("manufacturer"),
                "raw_data_json": {
                    "contract_details": contract_details,
                    "document_text_preview": document_text[:500] if document_text else "",
                    "contract_specs": contract_specs,
                    "comparison_result": comparison_result
                }
            }
            
            logger.info(f"Processed contract {reestr_number}: match_type={match_type}, score={ai_score}")
            return result
            
        except Exception as e:
            logger.error(f"Error processing contract: {e}")
            return None
    
    def execute_search(self, search_params: Dict[str, Any], tz_text: str = "") -> Dict[str, Any]:
        """
        Execute the complete search and analysis workflow.
        
        Args:
            search_params: Search parameters
            tz_text: Technical specification text
            
        Returns:
            Search results summary
        """
        try:
            # Update status to RUNNING
            self.search_request.status = SearchStatus.RUNNING
            self.db.commit()
            
            # Publish start event
            run_async(publish_search_status(
                self.search_id,
                "RUNNING",
                "Search started"
            ))
            
            # Step 1: Extract specifications from TZ using AI
            tz_specs = []
            if tz_text:
                try:
                    tz_specs = extract_specs_from_tz(tz_text)
                    logger.info(f"Extracted {len(tz_specs)} specifications from TZ")
                    
                    # Publish TZ extraction event
                    run_async(publish_search_status(
                        self.search_id,
                        "PROCESSING",
                        f"Extracted {len(tz_specs)} specifications from TZ"
                    ))
                except Exception as e:
                    logger.warning(f"Failed to extract specs from TZ: {e}")
                    run_async(publish_search_error(
                        self.search_id,
                        f"Failed to extract TZ specifications: {str(e)}"
                    ))
            
            # Step 2: Search for contracts
            logger.info(f"Starting contract search with params: {search_params}")
            
            # Publish search start event
            run_async(publish_search_status(
                self.search_id,
                "PROCESSING",
                "Searching for contracts"
            ))
            
            # Convert search params to SearchParams object
            params = SearchParams(
                law_type=search_params.get("law_type", "44-FZ"),
                region=search_params.get("region"),
                date_from=search_params.get("date_from"),
                date_to=search_params.get("date_to"),
                ktru=search_params.get("ktru_code"),
                limit_contracts=search_params.get("limit_contracts", 30)
            )
            
            # Perform search
            search_result = self.searcher.search(params)
            
            # Update found total
            self.search_request.found_total = search_result.found_total
            self.db.commit()
            
            logger.info(f"Found {search_result.found_total} contracts, processing {len(search_result.contracts)}")
            
            # Publish search results event
            run_async(publish_search_status(
                self.search_id,
                "PROCESSING",
                f"Found {search_result.found_total} contracts",
                {"found_total": search_result.found_total, "to_process": len(search_result.contracts)}
            ))
            
            # Step 3: Process each contract
            processed_contracts = []
            contract_results = []
            
            for i, contract_info in enumerate(search_result.contracts):
                # Check stop signal
                if self.check_stop_signal():
                    logger.info(f"Search {self.search_id} stopped by user")
                    self.search_request.status = SearchStatus.STOPPED
                    self.db.commit()
                    
                    # Publish stopped event
                    run_async(publish_search_status(
                        self.search_id,
                        "STOPPED",
                        "Search stopped by user",
                        {"processed_count": i, "found_total": search_result.found_total}
                    ))
                    
                    return {
                        "status": "stopped",
                        "processed_count": i,
                        "found_total": search_result.found_total
                    }
                
                # Process contract
                contract_dict = contract_info.dict() if hasattr(contract_info, 'dict') else contract_info
                result = self.process_contract(contract_dict, tz_specs)
                
                if result:
                    # Create ContractResult record
                    contract_result = ContractResult(
                        search_id=self.search_id,
                        reestr_number=result["reestr_number"],
                        contract_url=result["contract_url"],
                        sign_date=result["sign_date"],
                        unit_price=result["unit_price"],
                        match_type=result["match_type"],
                        ai_score=result["ai_score"],
                        manufacturer_target=result["manufacturer_target"],
                        manufacturer_found=result["manufacturer_found"],
                        raw_data_json=result["raw_data_json"]
                    )
                    
                    self.db.add(contract_result)
                    self.db.flush()  # Get ID without committing
                    
                    # Create spec comparison rows if available
                    if result["raw_data_json"].get("comparison_result", {}).get("comparisons"):
                        for comp in result["raw_data_json"]["comparison_result"]["comparisons"]:
                            spec_row = SpecComparisonRow(
                                contract_result_id=contract_result.id,
                                name=comp.get("name", ""),
                                target_value=comp.get("target_value", ""),
                                actual_value=comp.get("actual_value", ""),
                                match_status=comp.get("match_status", "NO_MATCH"),
                                weight=comp.get("weight", 1.0)
                            )
                            self.db.add(spec_row)
                    
                    contract_results.append(contract_result)
                    processed_contracts.append(result)
                
                # Update progress every 5 contracts
                if (i + 1) % 5 == 0 or (i + 1) == len(search_result.contracts):
                    self.update_progress(i + 1, f"Processed {i + 1}/{len(search_result.contracts)} contracts")
                    
                    # Publish progress event
                    run_async(publish_search_progress(
                        self.search_id,
                        i + 1,
                        len(search_result.contracts),
                        f"Processed {i + 1}/{len(search_result.contracts)} contracts"
                    ))
            
            # Step 4: Calculate NMC value from top matching contracts
            nmc_value = None
            if processed_contracts:
                # Sort by AI score descending
                sorted_contracts = sorted(
                    processed_contracts,
                    key=lambda x: x.get("ai_score", 0),
                    reverse=True
                )
                
                # Take top 3 for NMC calculation
                top_contracts = sorted_contracts[:3]
                
                if top_contracts:
                    nmc_value = calculate_nmc(top_contracts, method="average")
                    self.search_request.nmc_value = nmc_value
            
            # Step 5: Update final status
            self.search_request.status = SearchStatus.COMPLETED
            self.search_request.processed_count = len(processed_contracts)
            self.db.commit()
            
            logger.info(f"Search {self.search_id} completed: processed {len(processed_contracts)} contracts")
            
            # Publish completion event
            run_async(publish_search_status(
                self.search_id,
                "COMPLETED",
                f"Search completed successfully. Processed {len(processed_contracts)} contracts.",
                {
                    "processed_count": len(processed_contracts),
                    "found_total": search_result.found_total,
                    "nmc_value": str(nmc_value) if nmc_value else None,
                    "contract_results_count": len(contract_results)
                }
            ))
            
            return {
                "status": "completed",
                "processed_count": len(processed_contracts),
                "found_total": search_result.found_total,
                "nmc_value": str(nmc_value) if nmc_value else None,
                "contract_results_count": len(contract_results)
            }
            
        except Exception as e:
            logger.error(f"Error executing search {self.search_id}: {e}")
            
            # Publish error event
            run_async(publish_search_error(
                self.search_id,
                f"Search failed: {str(e)}",
                {"error_details": str(e)}
            ))
            
            # Update status to FAILED
            try:
                self.search_request.status = SearchStatus.FAILED
                self.db.commit()
            except Exception as inner_e:
                logger.error(f"Failed to update status to FAILED: {inner_e}")
            
            raise
    
    def get_search_summary(self) -> Dict[str, Any]:
        """Get summary of search results."""
        # Count contracts by match type
        from sqlalchemy import func
        
        match_type_counts = self.db.query(
            ContractResult.match_type,
            func.count(ContractResult.id).label('count')
        ).filter(
            ContractResult.search_id == self.search_id
        ).group_by(
            ContractResult.match_type
        ).all()
        
        # Calculate average AI score
        avg_score = self.db.query(
            func.avg(ContractResult.ai_score)
        ).filter(
            ContractResult.search_id == self.search_id,
            ContractResult.ai_score.isnot(None)
        ).scalar()
        
        return {
            "search_id": self.search_id,
            "status": self.search_request.status.value,
            "found_total": self.search_request.found_total,
            "processed_count": self.search_request.processed_count,
            "nmc_value": str(self.search_request.nmc_value) if self.search_request.nmc_value else None,
            "match_type_counts": {mt.value: count for mt, count in match_type_counts},
            "average_ai_score": float(avg_score) if avg_score else None,
            "created_at": self.search_request.created_at.isoformat() if self.search_request.created_at else None
        }