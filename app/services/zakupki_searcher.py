import os
import re
import json
import uuid
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime

import time
import httpx
from bs4 import BeautifulSoup
import pandas as pd
 
 
class ZakupkiSearcher:
    """Scraper for contract details from zakupki.gov.ru"""
     
    BASE_URL = "https://zakupki.gov.ru"
     
    def __init__(self, search_id: uuid.UUID, storage_base: str = "storage/temp"):
        """
        Initialize ZakupkiSearcher
        
        Args:
            search_id: UUID of the search request
            storage_base: Base directory for storing downloaded files
        """
        self.search_id = search_id
        self.storage_base = Path(storage_base)
        self.client = httpx.Client(timeout=30.0, follow_redirects=True)
         
    def _make_request(self, url: str, retries: int = 3, delay: int = 2) -> httpx.Response:
        """Make a request with retries and delay"""
        for i in range(retries):
            try:
                time.sleep(1)  # Rate limiting
                response = self.client.get(url)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                if e.response.status_code in [404, 502, 503]:
                    if i < retries - 1:
                        time.sleep(delay)
                        continue
                raise
            except httpx.RequestError as e:
                if i < retries - 1:
                    time.sleep(delay)
                    continue
                raise
     
    def fetch_contract_card(self, reestr_number: str) -> Dict:
        """
        Fetch contract card details from common-info.html
        
        Args:
            reestr_number: Contract registry number
            
        Returns:
            Dictionary with contract details including dates and customer
        """
        # Construct URL for contract card
        url = f"{self.BASE_URL}/epz/order/notice/ea44/view/common-info.html?regNumber={reestr_number}"
        
        try:
            response = self._make_request(url)
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract contract details
            contract_details = self._parse_common_info(soup)
            contract_details['reestr_number'] = reestr_number
            contract_details['common_info_html'] = response.text
            
            # Save HTML fixture
            self._save_fixture(reestr_number, "common-info.html", response.text)
            
            return contract_details
            
        except httpx.RequestError as e:
            raise Exception(f"Failed to fetch contract card: {e}")
        except Exception as e:
            raise Exception(f"Error parsing contract card: {e}")
    
    def _parse_common_info(self, soup: BeautifulSoup) -> Dict:
        """Parse common-info.html page"""
        details = {}
        
        # Extract customer name
        customer_elem = soup.find('span', string=re.compile(r'Заказчик', re.I))
        if customer_elem:
            customer_name = customer_elem.find_next('span', class_='cardMainInfo__content')
            if customer_name:
                details['customer_name'] = customer_name.get_text(strip=True)
        
        # Extract dates
        date_patterns = {
            'publication_date': r'Дата размещения',
            'update_date': r'Дата обновления',
            'application_deadline': r'Срок подачи заявок',
            'contract_date': r'Дата заключения контракта'
        }
        
        for key, pattern in date_patterns.items():
            date_elem = soup.find('span', string=re.compile(pattern, re.I))
            if date_elem:
                date_value = date_elem.find_next('span', class_='cardMainInfo__content')
                if date_value:
                    details[key] = date_value.get_text(strip=True)
        
        return details
    
    def fetch_contract_objects(self, reestr_number: str, ktru_code: Optional[str] = None) -> Dict:
        """
        Fetch contract objects (payments and objects tab)
        
        Args:
            reestr_number: Contract registry number
            ktru_code: Optional KTRU code to filter by
            
        Returns:
            Dictionary with objects table data and extracted unit price
        """
        # Try different possible URLs for objects tab
        urls_to_try = [
            f"{self.BASE_URL}/epz/order/notice/ea44/view/documents.html?regNumber={reestr_number}",
            f"{self.BASE_URL}/epz/order/notice/ea44/view/supplier-results.html?regNumber={reestr_number}",
            f"{self.BASE_URL}/epz/order/notice/ea44/view/print-form.html?regNumber={reestr_number}"
        ]
        
        objects_html = None
        objects_url = None
        
        for url in urls_to_try:
            try:
                response = self._make_request(url)
                if response.status_code == 200:
                    objects_html = response.text
                    objects_url = url
                    break
            except:
                continue
        
        if not objects_html:
            raise Exception(f"Could not fetch objects tab for contract {reestr_number}")
        
        # Parse objects HTML
        soup = BeautifulSoup(objects_html, 'html.parser')
        
        # Save HTML fixture
        self._save_fixture(reestr_number, "objects.html", objects_html)
        
        # Parse objects table
        objects_data = self._parse_objects_table(soup, ktru_code)
        objects_data['objects_html'] = objects_html
        objects_data['objects_url'] = objects_url
        
        return objects_data
    
    def _parse_objects_table(self, soup: BeautifulSoup, ktru_code: Optional[str] = None) -> Dict:
        """Parse objects table from HTML"""
        result = {
            'objects': [],
            'unit_price': None,
            'specification_text': None,
            'ktru_found': False
        }
        
        # Look for tables that might contain objects data
        tables = soup.find_all('table')
        
        for table in tables:
            # Try to parse as objects table
            try:
                df = pd.read_html(str(table))[0]
                
                # Check if this looks like an objects table
                if any(col for col in df.columns if 'КТРУ' in str(col) or 'KTRU' in str(col)):
                    result['objects'] = df.to_dict('records')
                    
                    # Find row matching KTRU code if provided
                    if ktru_code:
                        for obj in result['objects']:
                            obj_str = str(obj).lower()
                            if ktru_code.lower() in obj_str:
                                result['ktru_found'] = True
                                
                                # Extract unit price
                                for key, value in obj.items():
                                    key_lower = str(key).lower()
                                    if 'цена' in key_lower or 'price' in key_lower or 'стоимость' in key_lower:
                                        result['unit_price'] = value
                                        break
                                
                                # Extract specification text
                                spec_keys = ['наименование', 'name', 'описание', 'description']
                                for key in spec_keys:
                                    if key in str(obj).lower():
                                        result['specification_text'] = obj.get(key, '')
                                        break
                                
                                break
                    
                    break
            except:
                continue
        
        return result
    
    def fetch_attachments(self, reestr_number: str) -> List[Dict]:
        """
        Fetch contract attachments
        
        Args:
            reestr_number: Contract registry number
            
        Returns:
            List of attachment dictionaries with name and download URL
        """
        attachments = []
        
        # Try attachments tab URL
        url = f"{self.BASE_URL}/epz/order/notice/ea44/view/documents.html?regNumber={reestr_number}"
        
        try:
            response = self._make_request(url)
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for attachment links
            attachment_links = soup.find_all('a', href=True)
            
            for link in attachment_links:
                href = link['href']
                text = link.get_text(strip=True)
                
                # Check if this looks like an attachment
                if any(ext in href.lower() for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
                    attachments.append({
                        'name': text or os.path.basename(href),
                        'url': href if href.startswith('http') else f"{self.BASE_URL}{href}",
                        'type': self._get_file_type(href)
                    })
                # Check for "Печатная форма" (print form)
                elif 'печатная форма' in text.lower() or 'print form' in text.lower():
                    attachments.append({
                        'name': text,
                        'url': href if href.startswith('http') else f"{self.BASE_URL}{href}",
                        'type': 'print_form'
                    })
        
        except Exception as e:
            print(f"Warning: Could not fetch attachments: {e}")
        
        return attachments
    
    def download_attachment(self, attachment: Dict, reestr_number: str) -> Optional[str]:
        """
        Download an attachment to local storage
        
        Args:
            attachment: Attachment dictionary with name and url
            reestr_number: Contract registry number
            
        Returns:
            Path to downloaded file or None if download failed
        """
        try:
            # Create directory for this contract
            contract_dir = self.storage_base / str(self.search_id) / reestr_number
            contract_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            filename = self._sanitize_filename(attachment['name'])
            if not filename:
                filename = f"attachment_{uuid.uuid4().hex[:8]}"
            
            # Add extension if missing
            if not any(filename.lower().endswith(ext) for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
                if attachment['type'] == 'pdf':
                    filename += '.pdf'
                elif attachment['type'] == 'doc':
                    filename += '.doc'
                elif attachment['type'] == 'docx':
                    filename += '.docx'
            
            filepath = contract_dir / filename
            
            # Download file
            response = self._make_request(attachment['url'])
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return str(filepath)
            
        except Exception as e:
            print(f"Warning: Failed to download attachment {attachment.get('name')}: {e}")
            return None
    
    def parse_contract_details(self, reestr_number: str, ktru_code: Optional[str] = None) -> Dict:
            """
            Parse complete contract details
            
            Args:
                reestr_number: Contract registry number
                ktru_code: Optional KTRU code to filter by
                
            Returns:
                Complete contract details dictionary
            """
            result = {
                'reestr_number': reestr_number,
                'success': False,
                'error': None,
                'contract_card': None,
                'objects': None,
                'attachments': [],
                'downloaded_files': [],
                'warnings': []
            }
            
            try:
                # Fetch contract card
                result['contract_card'] = self.fetch_contract_card(reestr_number)
                
                # Fetch objects
                result['objects'] = self.fetch_contract_objects(reestr_number, ktru_code)
                
                # Check for price not found
                if not result['objects'].get('unit_price'):
                    result['warnings'].append('Price not found in objects table')
                
                # Check for specification text not found
                if not result['objects'].get('specification_text'):
                    result['warnings'].append('Specification text not found in objects table')
                
                # Check if we need to look for attachments
                need_attachments = (
                    not result['objects'].get('specification_text') or
                    not result['objects'].get('unit_price') or
                    self._is_recent_contract(result['contract_card'])
                )
                
                if need_attachments:
                    # Fetch and download attachments
                    attachments = self.fetch_attachments(reestr_number)
                    result['attachments'] = attachments
                    
                    for attachment in attachments:
                        filepath = self.download_attachment(attachment, reestr_number)
                        if filepath:
                            result['downloaded_files'].append(filepath)
                    
                    # Check if attachments were found
                    if not attachments:
                        result['warnings'].append('No attachments found for missing price/specification')
                    elif not result['downloaded_files']:
                        result['warnings'].append('Attachments found but could not be downloaded')
                
                result['success'] = True
                
            except Exception as e:
                result['error'] = str(e)
                result['success'] = False
            
            return result
    
    def _is_recent_contract(self, contract_details: Dict) -> bool:
        """Check if contract is from 2025 or later"""
        date_fields = ['publication_date', 'contract_date', 'update_date']
        
        for field in date_fields:
            date_str = contract_details.get(field)
            if date_str:
                # Try to extract year from date string
                year_match = re.search(r'20(\d{2})', date_str)
                if year_match:
                    year = int(year_match.group(0))
                    return year >= 2025
        
        return False
    
    def _save_fixture(self, reestr_number: str, filename: str, content: str):
        """Save HTML content as fixture for testing"""
        fixture_dir = Path("tests/fixtures") / reestr_number
        fixture_dir.mkdir(parents=True, exist_ok=True)
        
        fixture_path = fixture_dir / filename
        with open(fixture_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _get_file_type(self, url: str) -> str:
        """Determine file type from URL"""
        url_lower = url.lower()
        
        if '.pdf' in url_lower:
            return 'pdf'
        elif '.docx' in url_lower:
            return 'docx'
        elif '.doc' in url_lower:
            return 'doc'
        elif '.xlsx' in url_lower:
            return 'xlsx'
        elif '.xls' in url_lower:
            return 'xls'
        else:
            return 'unknown'
    
    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for safe storage"""
        if not filename:
            return ""
        
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        
        # Limit length
        if len(filename) > 200:
            name, ext = os.path.splitext(filename)
            filename = name[:200 - len(ext)] + ext
        
        return filename.strip()
    
    def close(self):
        """Close HTTP client"""
        if self.client:
            self.client.close()