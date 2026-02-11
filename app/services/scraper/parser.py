import httpx
from bs4 import BeautifulSoup
import tempfile
import os
from typing import Dict, Optional, List
from urllib.parse import urljoin, urlparse


class ContractParser:
    """Parser for contract details and attachments from procurement websites."""
    
    def __init__(self, client: Optional[httpx.AsyncClient] = None):
        self.client = client or httpx.AsyncClient(timeout=30.0)
        self.last_error = None
    
    async def parse_card(self, url: str) -> Dict:
        """
        Parse contract card details from a given URL.
        
        Args:
            url: The URL of the contract card page
            
        Returns:
            Dictionary containing parsed contract details including:
            - date: Contract date
            - customer: Customer/organization name
            - positions: List of positions with KTRU and unit_price
            - attachments: List of attachment file data
        """
        result = {
            "url": url,
            "date": None,
            "customer": None,
            "positions": [],
            "attachments": []
        }
        
        try:
            # 1. Fetch and parse common-info.html
            common_info_url = self._get_common_info_url(url)
            common_info_html = await self._fetch_html(common_info_url)
            
            if common_info_html:
                result.update(self._parse_common_info(common_info_html))
            
            # 2. Fetch and parse Payments and Objects tab
            objects_url = await self._find_objects_url(url, common_info_html)
            if objects_url:
                objects_html = await self._fetch_html(objects_url)
                if objects_html:
                    result["positions"] = self._parse_objects_table(objects_html)
            
            # 3. Fetch and parse Attachments tab
            attachments_url = await self._find_attachments_url(url, common_info_html)
            if attachments_url:
                attachments_html = await self._fetch_html(attachments_url)
                if attachments_html:
                    result["attachments"] = await self._parse_attachments(attachments_html, url)
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _get_common_info_url(self, base_url: str) -> str:
        """Construct common-info.html URL from base URL."""
        parsed = urlparse(base_url)
        # Assuming common-info.html is in the same directory
        return urljoin(base_url, "common-info.html")
    
    async def _fetch_html(self, url: str) -> Optional[str]:
        """Fetch HTML content from URL."""
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.text
        except Exception as e:
            # Store error for debugging
            self.last_error = str(e)
            return None
    
    def _parse_common_info(self, html: str) -> Dict:
        """Parse Date and Customer from common-info.html."""
        soup = BeautifulSoup(html, 'lxml')
        result = {"date": None, "customer": None}
        
        # Try to find date - common patterns
        date_selectors = [
            "td:contains('Дата') + td",
            "td:contains('Date') + td",
            "th:contains('Дата') ~ td",
            "th:contains('Date') ~ td",
            ".date",
            "[class*='date']"
        ]
        
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem and date_elem.text.strip():
                result["date"] = date_elem.text.strip()
                break
        
        # Try to find customer - common patterns
        customer_selectors = [
            "td:contains('Заказчик') + td",
            "td:contains('Customer') + td",
            "td:contains('Организация') + td",
            "th:contains('Заказчик') ~ td",
            "th:contains('Customer') ~ td",
            ".customer",
            "[class*='customer']"
        ]
        
        for selector in customer_selectors:
            customer_elem = soup.select_one(selector)
            if customer_elem and customer_elem.text.strip():
                result["customer"] = customer_elem.text.strip()
                break
        
        return result
    
    async def _find_objects_url(self, base_url: str, common_info_html: Optional[str] = None) -> Optional[str]:
        """Find URL for Payments and Objects tab."""
        # Method 1: Try to find link in common-info.html
        if common_info_html:
            soup = BeautifulSoup(common_info_html, 'lxml')
            # Look for links containing keywords
            keywords = ["objects", "payments", "позиции", "объекты", "платежи"]
            for link in soup.find_all('a', href=True):
                href = link['href'].lower()
                if any(keyword in href for keyword in keywords):
                    return urljoin(base_url, link['href'])
        
        # Method 2: Try common URL patterns
        common_patterns = [
            "objects.html",
            "payments.html",
            "positions.html",
            "table.html"
        ]
        
        for pattern in common_patterns:
            test_url = urljoin(base_url, pattern)
            try:
                response = await self.client.head(test_url)
                if response.status_code == 200:
                    return test_url
            except Exception:
                continue
        
        return None
    
    def _parse_objects_table(self, html: str) -> List[Dict]:
        """Parse HTML table for Positions, KTRU, Unit Price."""
        soup = BeautifulSoup(html, 'lxml')
        positions = []
        
        # Find all tables
        tables = soup.find_all('table')
        for table in tables:
            # Try to find header row
            headers = []
            header_row = table.find('tr')
            if header_row:
                headers = [th.get_text(strip=True).lower() for th in header_row.find_all(['th', 'td'])]
            
            # Check if this table has relevant columns
            relevant_headers = ['позиция', 'position', 'ктру', 'ktru', 'цена', 'price', 'стоимость']
            if not any(any(rh in h for rh in relevant_headers) for h in headers if h):
                # Try to infer from data rows
                pass
            
            # Parse data rows
            rows = table.find_all('tr')[1:]  # Skip header
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:  # Need at least position, ktru, price
                    try:
                        position = cells[0].get_text(strip=True)
                        ktru = cells[1].get_text(strip=True) if len(cells) > 1 else ""
                        unit_price = cells[2].get_text(strip=True) if len(cells) > 2 else ""
                        
                        # Clean up price - remove non-numeric characters except decimal point
                        if unit_price:
                            # Try to extract numeric value
                            import re
                            # Match numbers with spaces/thousand separators and comma as decimal separator
                            # Pattern: digits with optional spaces, optional comma with decimals
                            price_match = re.search(r'[\d\s]+(?:,\d+)?', unit_price)
                            if price_match:
                                # Remove spaces and replace comma with period for decimal
                                unit_price = price_match.group(0).replace(' ', '').replace(',', '.')
                        
                        positions.append({
                            "position": position,
                            "ktru": ktru,
                            "unit_price": unit_price
                        })
                    except (IndexError, AttributeError):
                        continue
        
        return positions
    
    async def _find_attachments_url(self, base_url: str, common_info_html: Optional[str] = None) -> Optional[str]:
        """Find URL for Attachments tab."""
        # Method 1: Try to find link in common-info.html
        if common_info_html:
            soup = BeautifulSoup(common_info_html, 'lxml')
            # Look for links containing keywords
            keywords = ["attachments", "files", "документы", "файлы", "вложения"]
            for link in soup.find_all('a', href=True):
                href = link['href'].lower()
                if any(keyword in href for keyword in keywords):
                    return urljoin(base_url, link['href'])
        
        # Method 2: Try common URL patterns
        common_patterns = [
            "attachments.html",
            "files.html",
            "documents.html"
        ]
        
        for pattern in common_patterns:
            test_url = urljoin(base_url, pattern)
            try:
                response = await self.client.head(test_url)
                if response.status_code == 200:
                    return test_url
            except Exception:
                continue
        
        return None
    
    async def _parse_attachments(self, html: str, base_url: str) -> List[Dict]:
        """Parse attachments tab and download relevant files."""
        soup = BeautifulSoup(html, 'lxml')
        attachments = []
        
        # Look for file links
        current_year = 2025  # As per requirements
        keywords = ["printed form", "печатная форма", "форма", "договор", "contract"]
        
        for link in soup.find_all('a', href=True):
            link_text = link.get_text(strip=True).lower()
            href = link['href']
            
            # Check if this is a relevant file for 2025+ contracts
            if any(keyword in link_text for keyword in keywords):
                # Check for year in link text or nearby elements
                year_patterns = [str(year) for year in range(current_year, current_year + 5)]
                has_recent_year = any(year in link_text for year in year_patterns)
                
                # Also check parent elements for year
                if not has_recent_year:
                    parent_text = " ".join([p.get_text() for p in link.find_parents()[:2]]).lower()
                    has_recent_year = any(year in parent_text for year in year_patterns)
                
                if has_recent_year:
                    file_url = urljoin(base_url, href)
                    try:
                        file_data = await self._download_file(file_url)
                        if file_data:
                            attachments.append({
                                "name": link_text,
                                "url": file_url,
                                "content": file_data,
                                "size": len(file_data)
                            })
                    except Exception as e:
                        # Log error but continue
                        attachments.append({
                            "name": link_text,
                            "url": file_url,
                            "error": str(e)
                        })
        
        return attachments
    
    async def _download_file(self, url: str) -> Optional[bytes]:
        """Download file content."""
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.content
        except Exception:
            return None
    
    async def close(self):
        """Close HTTP client."""
        await self.client.aclose()


async def parse_card(url: str) -> Dict:
    """Convenience function to parse contract card."""
    parser = ContractParser()
    try:
        result = await parser.parse_card(url)
        return result
    finally:
        await parser.close()