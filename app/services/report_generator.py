"""
Report Generator Service for NMCC Calculation and Export

This module provides functionality to generate NMCC (Normalized Maximum Contract Cost)
reports in XLSX format with summary and comparison matrix sheets.
"""

import uuid
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from io import BytesIO

from sqlalchemy.orm import Session
from sqlalchemy import desc
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

from app.models.contract import ContractResult, SpecComparisonRow
from app.models.search import SearchRequest


class ReportGenerator:
    """Generator for NMCC calculation and report export"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_nmcc_calculation(self, search_id: uuid.UUID) -> Dict[str, Any]:
        """
        Calculate NMCC (Normalized Maximum Contract Cost) for a search.
        
        Logic:
        1. Select top 3 contracts with highest ai_score AND accepted_for_nmc=True
        2. Calculate average contract_price of these top 3 contracts
        3. Return NMCC value and contract details
        
        Args:
            search_id: UUID of the search request
            
        Returns:
            Dictionary containing:
            - nmcc_value: Calculated NMCC (average of top 3 contract prices)
            - top_contracts: List of top 3 contracts with details
            - total_contracts: Total number of contracts for this search
            - contracts_with_flag: Number of contracts with accepted_for_nmc=True
        """
        # Get all contracts for this search, ordered by ai_score descending
        contracts = self.db.query(ContractResult)\
            .filter(ContractResult.search_id == search_id)\
            .filter(ContractResult.accepted_for_nmc == True)\
            .order_by(desc(ContractResult.ai_score))\
            .all()
        
        total_contracts = self.db.query(ContractResult)\
            .filter(ContractResult.search_id == search_id)\
            .count()
        
        contracts_with_flag = len(contracts)
        
        # Take top 3 contracts
        top_contracts = contracts[:3]
        
        # Calculate NMCC as average of top 3 contract prices
        nmcc_value = None
        if top_contracts:
            valid_prices = [c.contract_price for c in top_contracts if c.contract_price is not None]
            if valid_prices:
                nmcc_value = sum(valid_prices) / len(valid_prices)
        
        # Prepare contract details
        contract_details = []
        for i, contract in enumerate(top_contracts, 1):
            contract_details.append({
                'rank': i,
                'reestr_number': contract.reestr_number,
                'contract_number': contract.contract_number,
                'supplier_name': contract.supplier_name,
                'contract_price': contract.contract_price,
                'currency': contract.currency,
                'ai_score': contract.ai_score,
                'match_type': contract.match_type.value if contract.match_type else None,
                'contract_date': contract.contract_date,
            })
        
        return {
            'nmcc_value': nmcc_value,
            'top_contracts': contract_details,
            'total_contracts': total_contracts,
            'contracts_with_flag': contracts_with_flag,
            'search_id': str(search_id),
            'calculation_date': datetime.now().isoformat()
        }
    
    def generate_comparison_matrix(self, search_id: uuid.UUID, top_contracts: List[Dict]) -> pd.DataFrame:
        """
        Generate comparison matrix for specifications.
        
        Rows = Specifications (from SpecComparisonRow)
        Columns = Top contracts
        
        Args:
            search_id: UUID of the search request
            top_contracts: List of top contract details from get_nmcc_calculation
            
        Returns:
            pandas DataFrame with comparison matrix
        """
        if not top_contracts:
            return pd.DataFrame()
        
        # Get all specification rows for the top contracts
        contract_ids = []
        for contract in top_contracts:
            # Find contract by reestr_number
            contract_obj = self.db.query(ContractResult)\
                .filter(ContractResult.search_id == search_id)\
                .filter(ContractResult.reestr_number == contract['reestr_number'])\
                .first()
            if contract_obj:
                contract_ids.append(contract_obj.id)
        
        # Get all unique specification names
        spec_rows = self.db.query(SpecComparisonRow)\
            .filter(SpecComparisonRow.contract_result_id.in_(contract_ids))\
            .all()
        
        unique_specs = list(set([row.name for row in spec_rows]))
        unique_specs.sort()
        
        # Create comparison matrix
        matrix_data = []
        for spec_name in unique_specs:
            row_data = {'Specification': spec_name}
            
            for contract in top_contracts:
                # Find contract by reestr_number
                contract_obj = self.db.query(ContractResult)\
                    .filter(ContractResult.search_id == search_id)\
                    .filter(ContractResult.reestr_number == contract['reestr_number'])\
                    .first()
                
                if contract_obj:
                    # Find spec row for this contract
                    spec_row = self.db.query(SpecComparisonRow)\
                        .filter(SpecComparisonRow.contract_result_id == contract_obj.id)\
                        .filter(SpecComparisonRow.name == spec_name)\
                        .first()
                    
                    if spec_row:
                        # Use actual value if available, otherwise target value
                        value = spec_row.actual_value if spec_row.actual_value else spec_row.target_value
                        match_status = spec_row.match_status.value if spec_row.match_status else 'unknown'
                        row_data[f"{contract['reestr_number']} ({match_status})"] = value
                    else:
                        row_data[f"{contract['reestr_number']} (not found)"] = "N/A"
                else:
                    row_data[f"{contract['reestr_number']} (error)"] = "N/A"
            
            matrix_data.append(row_data)
        
        return pd.DataFrame(matrix_data)
    
    def create_xlsx_report(self, search_id: uuid.UUID) -> BytesIO:
        """
        Create XLSX report with two sheets:
        1. Summary: NMCC calculation and input parameters
        2. Comparison Matrix: Specifications vs Contracts comparison
        
        Args:
            search_id: UUID of the search request
            
        Returns:
            BytesIO object containing the XLSX file
        """
        # Get search details
        search = self.db.query(SearchRequest).filter(SearchRequest.id == search_id).first()
        if not search:
            raise ValueError(f"Search with ID {search_id} not found")
        
        # Calculate NMCC
        nmcc_data = self.get_nmcc_calculation(search_id)
        
        # Generate comparison matrix
        comparison_df = self.generate_comparison_matrix(search_id, nmcc_data['top_contracts'])
        
        # Create workbook
        wb = Workbook()
        
        # ===== Sheet 1: Summary =====
        ws_summary = wb.active
        ws_summary.title = "Summary"
        
        # Header styling
        header_font = Font(bold=True, size=12)
        header_fill = PatternFill(start_color="366092", end_color="366092", fill_type="solid")
        header_font_color = Font(bold=True, color="FFFFFF")
        thin_border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
        
        # Write report title
        ws_summary.merge_cells('A1:D1')
        title_cell = ws_summary['A1']
        title_cell.value = f"NMCC Calculation Report - Search ID: {search_id}"
        title_cell.font = Font(bold=True, size=14)
        title_cell.alignment = Alignment(horizontal='center')
        
        # Write calculation date
        ws_summary['A3'] = "Calculation Date:"
        ws_summary['B3'] = nmcc_data['calculation_date']
        
        # Write NMCC value
        ws_summary['A5'] = "NMCC Value:"
        ws_summary['B5'] = nmcc_data['nmcc_value'] if nmcc_data['nmcc_value'] is not None else "N/A"
        if nmcc_data['nmcc_value'] is not None:
            ws_summary['B5'].number_format = '#,##0.00'
        
        # Write statistics
        ws_summary['A7'] = "Total Contracts:"
        ws_summary['B7'] = nmcc_data['total_contracts']
        ws_summary['A8'] = "Contracts with accepted_for_nmc=True:"
        ws_summary['B8'] = nmcc_data['contracts_with_flag']
        
        # Write search parameters header
        ws_summary['A10'] = "Search Parameters"
        ws_summary['A10'].font = header_font
        ws_summary['A10'].fill = header_fill
        ws_summary['A10'].font = header_font_color
        ws_summary['A10'].border = thin_border
        
        # Write search parameters
        params = [
            ("Input Source", search.input_source),
            ("KTRU Code", search.ktru_code),
            ("Search Query", search.search_query),
            ("Region Filter", search.region_filter),
            ("Date From", search.date_from),
            ("Date To", search.date_to),
            ("Price Min", search.price_min),
            ("Price Max", search.price_max),
            ("NMC Value", search.nmc_value),
            ("AI Model Version", search.ai_model_version),
            ("Confidence Threshold", search.confidence_threshold),
        ]
        
        for i, (param_name, param_value) in enumerate(params, start=11):
            ws_summary[f'A{i}'] = param_name
            ws_summary[f'B{i}'] = param_value if param_value is not None else "N/A"
            if isinstance(param_value, (int, float)):
                ws_summary[f'B{i}'].number_format = '#,##0.00'
        
        # Write top contracts header
        start_row = 11 + len(params) + 2
        ws_summary[f'A{start_row}'] = "Top 3 Contracts for NMCC Calculation"
        ws_summary[f'A{start_row}'].font = header_font
        ws_summary[f'A{start_row}'].fill = header_fill
        ws_summary[f'A{start_row}'].font = header_font_color
        ws_summary[f'A{start_row}'].border = thin_border
        ws_summary.merge_cells(f'A{start_row}:H{start_row}')
        
        # Write top contracts table headers
        headers = ["Rank", "Reestr Number", "Contract Number", "Supplier Name", 
                  "Contract Price", "Currency", "AI Score", "Match Type"]
        
        for col_idx, header in enumerate(headers, start=1):
            cell = ws_summary.cell(row=start_row+1, column=col_idx)
            cell.value = header
            cell.font = Font(bold=True)
            cell.border = thin_border
            cell.alignment = Alignment(horizontal='center')
        
        # Write top contracts data
        for row_idx, contract in enumerate(nmcc_data['top_contracts'], start=start_row+2):
            ws_summary.cell(row=row_idx, column=1, value=contract['rank'])
            ws_summary.cell(row=row_idx, column=2, value=contract['reestr_number'])
            ws_summary.cell(row=row_idx, column=3, value=contract['contract_number'])
            ws_summary.cell(row=row_idx, column=4, value=contract['supplier_name'])
            ws_summary.cell(row=row_idx, column=5, value=contract['contract_price'])
            if contract['contract_price'] is not None:
                ws_summary.cell(row=row_idx, column=5).number_format = '#,##0.00'
            ws_summary.cell(row=row_idx, column=6, value=contract['currency'])
            ws_summary.cell(row=row_idx, column=7, value=contract['ai_score'])
            if contract['ai_score'] is not None:
                ws_summary.cell(row=row_idx, column=7).number_format = '0.00'
            ws_summary.cell(row=row_idx, column=8, value=contract['match_type'])
        
        # Auto-adjust column widths
        for column in ws_summary.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            adjusted_width = min(max_length + 2, 50)
            ws_summary.column_dimensions[column_letter].width = adjusted_width
        
        # ===== Sheet 2: Comparison Matrix =====
        if not comparison_df.empty:
            ws_matrix = wb.create_sheet(title="Comparison Matrix")
            
            # Write title
            ws_matrix.merge_cells('A1:D1')
            title_cell = ws_matrix['A1']
            title_cell.value = f"Specification Comparison Matrix - Search ID: {search_id}"
            title_cell.font = Font(bold=True, size=14)
            title_cell.alignment = Alignment(horizontal='center')
            
            # Write DataFrame to Excel
            for r_idx, row in enumerate(comparison_df.itertuples(), start=3):
                for c_idx, value in enumerate(row[1:], start=1):  # Skip index
                    cell = ws_matrix.cell(row=r_idx, column=c_idx, value=value)
                    cell.border = thin_border
            
            # Write headers
            headers = list(comparison_df.columns)
            for c_idx, header in enumerate(headers, start=1):
                cell = ws_matrix.cell(row=2, column=c_idx, value=header)
                cell.font = Font(bold=True)
                cell.fill = header_fill
                cell.font = header_font_color
                cell.border = thin_border
                cell.alignment = Alignment(horizontal='center')
            
            # Auto-adjust column widths
            for column in ws_matrix.columns:
                max_length = 0
                column_letter = get_column_letter(column[0].column)
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                ws_matrix.column_dimensions[column_letter].width = adjusted_width
        
        # Save to BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        return output
    
    def generate_report(self, search_id: uuid.UUID) -> Tuple[BytesIO, str]:
        """
        Generate report and return file with filename.
        
        Args:
            search_id: UUID of the search request
            
        Returns:
            Tuple of (BytesIO object with XLSX, filename)
        """
        xlsx_file = self.create_xlsx_report(search_id)
        filename = f"nmcc_report_{search_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        return xlsx_file, filename