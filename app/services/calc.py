"""
NMTSK Calculation Service

This module provides functionality for calculating NMTSK (average price)
from selected contracts and generating Excel reports.
"""

import os
import uuid
from decimal import Decimal
from typing import List, Optional, Dict, Any
from datetime import datetime

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter

from app.models import ContractResult
from app.schemas import ContractResultResponse


def calculate_nmtsk_average(contracts: List[ContractResult]) -> Optional[Decimal]:
    """
    Calculate NMTSK average from top 3 selected contracts.
    
    Args:
        contracts: List of ContractResult objects with unit_price
        
    Returns:
        Decimal average of top 3 unit prices, or None if insufficient data
        
    Notes:
        - Takes top 3 contracts by unit_price (highest prices)
        - If fewer than 3 contracts provided, calculates average of available contracts
        - Returns None if no contracts with unit_price available
        - Filters out contracts with None unit_price
    """
    if not contracts:
        return None
    
    # Filter out contracts without unit_price and convert to list of prices
    prices = [contract.unit_price for contract in contracts if contract.unit_price is not None]
    
    if not prices:
        return None
    
    # Sort prices in descending order (highest first) and take top 3
    sorted_prices = sorted(prices, reverse=True)
    top_prices = sorted_prices[:3]
    
    # Calculate average
    total = sum(top_prices, Decimal('0'))
    average = total / len(top_prices)
    
    return average


def calculate_nmtsk_average_from_responses(contract_responses: List[ContractResultResponse]) -> Optional[Decimal]:
    """
    Calculate NMTSK average from top 3 selected contract responses.
    
    Args:
        contract_responses: List of ContractResultResponse objects with unit_price
        
    Returns:
        Decimal average of top 3 unit prices, or None if insufficient data
    """
    if not contract_responses:
        return None
    
    # Filter out contracts without unit_price and convert to list of prices
    prices = [resp.unit_price for resp in contract_responses if resp.unit_price is not None]
    
    if not prices:
        return None
    
    # Sort prices in descending order (highest first) and take top 3
    sorted_prices = sorted(prices, reverse=True)
    top_prices = sorted_prices[:3]
    
    # Calculate average
    total = sum(top_prices, Decimal('0'))
    average = total / len(top_prices)
    
    return average


def generate_excel_report(search_id: str, contracts: List[ContractResult], 
                         output_dir: str = "reports") -> str:
    """
    Generate Excel report for search results with Summary and Details sheets.
    
    Args:
        search_id: Search request ID
        contracts: List of ContractResult objects
        output_dir: Directory to save the report (default: "reports")
        
    Returns:
        Path to the generated Excel file
        
    Raises:
        ValueError: If contracts list is empty
    """
    if not contracts:
        raise ValueError("Cannot generate report: contracts list is empty")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nmtsk_report_{search_id}_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)
    
    # Calculate NMTSK average
    nmtsk_average = calculate_nmtsk_average(contracts)
    
    # Prepare data for Excel
    contracts_with_prices = [c for c in contracts if c.unit_price is not None]
    contracts_sorted = sorted(contracts_with_prices, key=lambda x: x.unit_price, reverse=True)
    
    # Create DataFrame for details sheet
    details_data = []
    for contract in contracts_sorted:
        details_data.append({
            "Реестровый номер": contract.reestr_number,
            "Дата подписания": contract.sign_date.strftime("%Y-%m-%d") if contract.sign_date else "Н/Д",
            "Цена за единицу": float(contract.unit_price) if contract.unit_price else None,
            "Тип соответствия": contract.match_type,
            "Оценка ИИ": contract.ai_score or "Н/Д",
            "Производитель (цель)": contract.manufacturer_target or "Н/Д",
            "Производитель (найден)": contract.manufacturer_found or "Н/Д",
            "Ссылка на контракт": contract.contract_url or "Н/Д"
        })
    
    details_df = pd.DataFrame(details_data)
    
    # Create summary data
    summary_data = {
        "Параметр": [
            "ID поиска",
            "Дата формирования отчета",
            "Всего контрактов",
            "Контрактов с ценой",
            "Средняя цена (НМЦ)",
            "Рассчитанная НМТСК",
            "Статус расчета"
        ],
        "Значение": [
            search_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            len(contracts),
            len(contracts_with_prices),
            float(contracts[0].search_request.nmc_value) if contracts and contracts[0].search_request.nmc_value else "Н/Д",
            float(nmtsk_average) if nmtsk_average else "Н/Д",
            "Успешно" if nmtsk_average else "Недостаточно данных"
        ]
    }
    
    summary_df = pd.DataFrame(summary_data)
    
    # Create Excel writer with openpyxl engine
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        # Write summary sheet
        summary_df.to_excel(writer, sheet_name='Сводка', index=False)
        
        # Write details sheet
        details_df.to_excel(writer, sheet_name='Детали', index=False)
        
        # Get workbook and sheets for formatting
        workbook = writer.book
        summary_sheet = workbook['Сводка']
        details_sheet = workbook['Детали']
        
        # Format summary sheet
        _format_summary_sheet(summary_sheet)
        
        # Format details sheet
        _format_details_sheet(details_sheet)
    
    return filepath


def _format_summary_sheet(sheet):
    """Apply formatting to summary sheet."""
    # Set column widths
    sheet.column_dimensions['A'].width = 30
    sheet.column_dimensions['B'].width = 40
    
    # Format header
    header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    
    for cell in sheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
    
    # Format data rows
    for row in sheet.iter_rows(min_row=2, max_row=sheet.max_row):
        for cell in row:
            cell.alignment = Alignment(horizontal="left", vertical="center")
    
    # Add borders and make it look nice
    from openpyxl.styles import Border, Side
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, min_col=1, max_col=2):
        for cell in row:
            cell.border = thin_border


def _format_details_sheet(sheet):
    """Apply formatting to details sheet."""
    # Set column widths
    column_widths = {
        'A': 20,  # Реестровый номер
        'B': 15,  # Дата подписания
        'C': 15,  # Цена за единицу
        'D': 15,  # Тип соответствия
        'E': 10,  # Оценка ИИ
        'F': 25,  # Производитель (цель)
        'G': 25,  # Производитель (найден)
        'H': 40,  # Ссылка на контракт
    }
    
    for col, width in column_widths.items():
        sheet.column_dimensions[col].width = width
    
    # Format header
    header_fill = PatternFill(start_color="4F81BD", end_color="4F81BD", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    
    for cell in sheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
    
    # Format price column as currency
    from openpyxl.styles import numbers
    for row in range(2, sheet.max_row + 1):
        price_cell = sheet[f'C{row}']
        if price_cell.value is not None:
            price_cell.number_format = numbers.FORMAT_NUMBER_COMMA_SEPARATED1
    
    # Add borders
    from openpyxl.styles import Border, Side
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    
    for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, min_col=1, max_col=8):
        for cell in row:
            cell.border = thin_border
            if cell.row > 1:  # Data rows
                cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)