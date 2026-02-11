"""
NMTSK Calculation Logic for Service Alpha.

This module provides functionality to calculate NMC (Normalized Maximum Contract) values
and generate reports.
"""

import json
import logging
from decimal import Decimal
from typing import List, Dict, Any, Optional
from datetime import datetime

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill

logger = logging.getLogger(__name__)


def calculate_nmc(contracts: List[Dict[str, Any]], method: str = "average") -> Optional[Decimal]:
    """
    Calculate NMC value from selected contracts.
    
    Args:
        contracts: List of contract dictionaries with unit_price
        method: Calculation method - "average", "median", or "trimmed_mean"
        
    Returns:
        Calculated NMC value as Decimal, or None if calculation fails
    """
    if not contracts:
        logger.warning("No contracts provided for NMC calculation")
        return None
    
    # Extract unit prices
    prices = []
    for contract in contracts:
        unit_price = contract.get("unit_price")
        if unit_price is not None:
            try:
                if isinstance(unit_price, (int, float, Decimal)):
                    prices.append(float(unit_price))
                elif isinstance(unit_price, str):
                    prices.append(float(unit_price))
            except (ValueError, TypeError):
                logger.warning(f"Invalid unit price in contract: {unit_price}")
                continue
    
    if not prices:
        logger.warning("No valid unit prices found in contracts")
        return None
    
    # Calculate based on method
    if method == "average":
        nmc_value = sum(prices) / len(prices)
    elif method == "median":
        sorted_prices = sorted(prices)
        n = len(sorted_prices)
        if n % 2 == 1:
            nmc_value = sorted_prices[n // 2]
        else:
            nmc_value = (sorted_prices[n // 2 - 1] + sorted_prices[n // 2]) / 2
    elif method == "trimmed_mean":
        # Remove outliers (top and bottom 10%)
        sorted_prices = sorted(prices)
        trim_count = int(len(sorted_prices) * 0.1)
        trimmed_prices = sorted_prices[trim_count:-trim_count] if trim_count > 0 else sorted_prices
        if trimmed_prices:
            nmc_value = sum(trimmed_prices) / len(trimmed_prices)
        else:
            nmc_value = sum(prices) / len(prices)
    else:
        logger.error(f"Unknown calculation method: {method}")
        return None
    
    # Round to 2 decimal places
    nmc_value = round(nmc_value, 2)
    
    logger.info(f"Calculated NMC value: {nmc_value} using {method} method from {len(prices)} contracts")
    return Decimal(str(nmc_value))


def generate_excel_report(search_id: str, search_data: Dict[str, Any], 
                         contract_results: List[Dict[str, Any]]) -> str:
    """
    Generate Excel report for search results.
    
    Args:
        search_id: Search request ID
        search_data: Search request data
        contract_results: List of contract results
        
    Returns:
        Path to generated Excel file
    """
    import tempfile
    import os
    
    # Create temporary file
    temp_dir = tempfile.mkdtemp()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"search_report_{search_id}_{timestamp}.xlsx"
    filepath = os.path.join(temp_dir, filename)
    
    try:
        # Create workbook
        wb = Workbook()
        
        # Summary sheet
        ws_summary = wb.active
        ws_summary.title = "Summary"
        
        # Add search information
        ws_summary.append(["Search Report", ""])
        ws_summary.append(["Search ID", search_id])
        ws_summary.append(["Object Name", search_data.get("object_name", "")])
        ws_summary.append(["KTRU Code", search_data.get("ktru_code", "")])
        ws_summary.append(["Status", search_data.get("status", "")])
        ws_summary.append(["Found Total", search_data.get("found_total", 0)])
        ws_summary.append(["Processed Count", search_data.get("processed_count", 0)])
        ws_summary.append(["NMC Value", str(search_data.get("nmc_value", ""))])
        ws_summary.append(["Created At", search_data.get("created_at", "")])
        ws_summary.append([])
        
        # Add contract summary
        ws_summary.append(["Contract Results Summary", ""])
        ws_summary.append(["Total Contracts", len(contract_results)])
        
        # Count by match type
        match_types = {}
        for contract in contract_results:
            match_type = contract.get("match_type", "NO_MATCH")
            match_types[match_type] = match_types.get(match_type, 0) + 1
        
        ws_summary.append([])
        ws_summary.append(["Match Type", "Count"])
        for match_type, count in match_types.items():
            ws_summary.append([match_type, count])
        
        # Details sheet
        ws_details = wb.create_sheet(title="Details")
        
        # Add headers
        headers = [
            "Reestr Number", "Contract URL", "Sign Date", "Unit Price",
            "Match Type", "AI Score", "Manufacturer Target", "Manufacturer Found"
        ]
        ws_details.append(headers)
        
        # Add contract data
        for contract in contract_results:
            row = [
                contract.get("reestr_number", ""),
                contract.get("contract_url", ""),
                contract.get("sign_date", ""),
                str(contract.get("unit_price", "")),
                contract.get("match_type", ""),
                contract.get("ai_score", ""),
                contract.get("manufacturer_target", ""),
                contract.get("manufacturer_found", "")
            ]
            ws_details.append(row)
        
        # Apply formatting
        for sheet in [ws_summary, ws_details]:
            # Auto-adjust column widths
            for column in sheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except Exception:
                        pass
                adjusted_width = min(max_length + 2, 50)
                sheet.column_dimensions[column_letter].width = adjusted_width
            
            # Style header row
            for cell in sheet[1]:
                cell.font = Font(bold=True)
                cell.fill = PatternFill(start_color="DDDDDD", end_color="DDDDDD", fill_type="solid")
        
        # Save workbook
        wb.save(filepath)
        
        logger.info(f"Excel report generated: {filepath}")
        return filepath
        
    except Exception as e:
        logger.error(f"Error generating Excel report: {e}")
        raise


def generate_json_report(search_id: str, search_data: Dict[str, Any], 
                        contract_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate JSON report for search results.
    
    Args:
        search_id: Search request ID
        search_data: Search request data
        contract_results: List of contract results
        
    Returns:
        JSON report as dictionary
    """
    report = {
        "search_id": search_id,
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "version": "1.0"
        },
        "search_summary": {
            "object_name": search_data.get("object_name"),
            "ktru_code": search_data.get("ktru_code"),
            "status": search_data.get("status"),
            "found_total": search_data.get("found_total"),
            "processed_count": search_data.get("processed_count"),
            "nmc_value": str(search_data.get("nmc_value")) if search_data.get("nmc_value") else None,
            "created_at": search_data.get("created_at")
        },
        "contracts_summary": {
            "total_contracts": len(contract_results),
            "by_match_type": {},
            "average_ai_score": None,
            "price_range": None
        },
        "contracts": []
    }
    
    # Calculate summary statistics
    ai_scores = []
    unit_prices = []
    match_type_counts = {}
    
    for contract in contract_results:
        # Count match types
        match_type = contract.get("match_type", "NO_MATCH")
        match_type_counts[match_type] = match_type_counts.get(match_type, 0) + 1
        
        # Collect AI scores
        ai_score = contract.get("ai_score")
        if ai_score is not None:
            ai_scores.append(ai_score)
        
        # Collect unit prices
        unit_price = contract.get("unit_price")
        if unit_price is not None:
            try:
                unit_prices.append(float(unit_price))
            except (ValueError, TypeError):
                pass
        
        # Add contract to report
        contract_report = {
            "reestr_number": contract.get("reestr_number"),
            "contract_url": contract.get("contract_url"),
            "sign_date": contract.get("sign_date"),
            "unit_price": str(contract.get("unit_price")) if contract.get("unit_price") else None,
            "match_type": match_type,
            "ai_score": ai_score,
            "manufacturer_target": contract.get("manufacturer_target"),
            "manufacturer_found": contract.get("manufacturer_found")
        }
        report["contracts"].append(contract_report)
    
    # Update summary
    report["contracts_summary"]["by_match_type"] = match_type_counts
    
    if ai_scores:
        report["contracts_summary"]["average_ai_score"] = sum(ai_scores) / len(ai_scores)
    
    if unit_prices:
        report["contracts_summary"]["price_range"] = {
            "min": min(unit_prices),
            "max": max(unit_prices),
            "average": sum(unit_prices) / len(unit_prices)
        }
    
    return report