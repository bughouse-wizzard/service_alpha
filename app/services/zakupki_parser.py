"""
Zakupki.gov.ru search page parser.
Implements ZakupkiSearcher class for scraping contract search results.
"""

import re
import time
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from urllib.parse import urlencode

import httpx
from bs4 import BeautifulSoup


@dataclass
class ContractCard:
    """Data Transfer Object for a single contract card."""
    reestr_number: str
    contract_date: date
    price: float
    link: str
    title: Optional[str] = None
    customer: Optional[str] = None
    supplier: Optional[str] = None


@dataclass
class SearchResult:
    """Data Transfer Object for search results."""
    total_count: int
    cards: List[ContractCard]


class ZakupkiSearcher:
    """
    Parser for zakupki.gov.ru contract search results.
    
    Handles:
    - URL construction with query parameters (44-FZ, region, KTRU, date range)
    - HTTP requests with proper User-Agent headers
    - HTML parsing with BeautifulSoup
    - Rate limiting (respects robots.txt with 1-2 second delays)
    """
    
    BASE_URL = "https://zakupki.gov.ru/epz/contract/search/results.html"
    
    def __init__(self, user_agent: str = None):
        """
        Initialize the searcher.
        
        Args:
            user_agent: Custom User-Agent string. If None, uses a default.
        """
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
        self.last_request_time = 0
        self.min_request_interval = 1.0  # seconds
        
    def _respect_rate_limit(self):
        """Ensure we respect rate limits by waiting between requests."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def build_search_url(
        self,
        fz_44: bool = True,
        region: Optional[str] = None,
        ktru: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        page: int = 1
    ) -> str:
        """
        Construct search URL with query parameters.
        
        Args:
            fz_44: Whether to search for 44-FZ contracts (default True)
            region: Region code (e.g., '77' for Moscow)
            ktru: KTRU code
            date_from: Start date for contract signing
            date_to: End date for contract signing
            page: Page number (default 1)
            
        Returns:
            Complete URL with query parameters
        """
        params = {
            "pageNumber": page,
            "sortDirection": "false",
            "recordsPerPage": "_50",
            "showLotsInfoHidden": "false",
            "sortBy": "UPDATE_DATE",
            "fz44": "on" if fz_44 else "off",
            "af": "on",  # advanced search
        }
        
        if region:
            params["regions"] = region
            
        if ktru:
            params["ktru"] = ktru
            
        if date_from:
            params["contractDateFrom"] = date_from.strftime("%d.%m.%Y")
            
        if date_to:
            params["contractDateTo"] = date_to.strftime("%d.%m.%Y")
        
        return f"{self.BASE_URL}?{urlencode(params)}"
    
    def _create_client(self) -> httpx.Client:
        """Create HTTP client with proper headers."""
        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
        return httpx.Client(
            headers=headers,
            follow_redirects=True,
            timeout=30.0
        )
    
    def fetch_search_page(self, url: str) -> str:
        """
        Fetch HTML content from the search page.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content as string
            
        Raises:
            httpx.HTTPError: If the request fails
        """
        self._respect_rate_limit()
        
        with self._create_client() as client:
            response = client.get(url)
            response.raise_for_status()
            return response.text
    
    def parse_total_count(self, html: str) -> int:
        """
        Parse total number of records from HTML.
        
        Args:
            html: HTML content
            
        Returns:
            Total count of records, or 0 if not found
        """
        # Look for pattern like "XXX записей" - handle various formats:
        # - "125 записей" (regular space)
        # - "125&nbsp;записей" (HTML entity)
        # - "125\xa0записей" (non-breaking space character)
        # - "1 250 записей" (with thousands separator)
        pattern = r'(\d+(?:[ \xa0]?\d+)*)\s*(?:&nbsp;)?\s*запис[ей|и|ь]'
        match = re.search(pattern, html, re.IGNORECASE)
        
        if match:
            # Extract the number part
            number_text = match.group(1)
            # Remove all non-digit characters (spaces, &nbsp;, \xa0, etc.)
            clean_number = re.sub(r'[^\d]', '', number_text)
            if clean_number:
                return int(clean_number)
        
        return 0
    
    def parse_contract_cards(self, html: str) -> List[ContractCard]:
        """
        Parse contract cards from search results HTML.
        
        Args:
            html: HTML content
            
        Returns:
            List of ContractCard objects
        """
        soup = BeautifulSoup(html, 'lxml')
        cards = []
        
        # Find all contract cards - adjust selector based on actual HTML structure
        # This is a placeholder selector - needs to be adjusted based on actual page structure
        card_elements = soup.select('.registry-entry__body')
        
        for card in card_elements:
            try:
                contract_card = self._parse_single_card(card)
                if contract_card:
                    cards.append(contract_card)
            except Exception as e:
                # Log error but continue processing other cards
                print(f"Error parsing card: {e}")
                continue
        
        return cards
    
    def _parse_single_card(self, card_element) -> Optional[ContractCard]:
        """
        Parse a single contract card element.
        
        Args:
            card_element: BeautifulSoup element for a single card
            
        Returns:
            ContractCard object or None if parsing fails
        """
        try:
            # Extract reestr number
            reestr_elem = card_element.select_one('.registry-entry__header-mid__number a')
            reestr_number = reestr_elem.text.strip() if reestr_elem else ""
            
            # Extract link
            link = reestr_elem.get('href') if reestr_elem else ""
            if link and not link.startswith('http'):
                link = f"https://zakupki.gov.ru{link}"
            
            # Extract date
            date_elem = card_element.select_one('.data-block__value')
            contract_date_str = date_elem.text.strip() if date_elem else ""
            
            # Parse date (format: DD.MM.YYYY)
            contract_date = None
            if contract_date_str:
                try:
                    contract_date = datetime.strptime(contract_date_str, "%d.%m.%Y").date()
                except ValueError:
                    pass
            
            # Extract price
            price_elem = card_element.select_one('.price-block__value')
            price_text = price_elem.text.strip() if price_elem else ""
            
            # Parse price (remove currency symbol and spaces)
            price = 0.0
            if price_text:
                # Remove non-digit characters except decimal point
                price_clean = re.sub(r'[^\d.,]', '', price_text)
                # Replace comma with dot for decimal
                price_clean = price_clean.replace(',', '.')
                try:
                    price = float(price_clean)
                except ValueError:
                    pass
            
            # Extract title
            title_elem = card_element.select_one('.registry-entry__body-value')
            title = title_elem.text.strip() if title_elem else ""
            
            return ContractCard(
                reestr_number=reestr_number,
                contract_date=contract_date,
                price=price,
                link=link,
                title=title
            )
            
        except Exception as e:
            print(f"Error parsing card details: {e}")
            return None
    
    def parse_list(self, html: str) -> SearchResult:
        """
        Parse search results HTML and return structured data.
        
        Args:
            html: HTML content of search results page
            
        Returns:
            SearchResult object with total count and list of cards
        """
        total_count = self.parse_total_count(html)
        cards = self.parse_contract_cards(html)
        
        return SearchResult(
            total_count=total_count,
            cards=cards
        )
    
    def search(
        self,
        fz_44: bool = True,
        region: Optional[str] = None,
        ktru: Optional[str] = None,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
        max_pages: int = 1
    ) -> SearchResult:
        """
        Perform search and return results.
        
        Args:
            fz_44: Whether to search for 44-FZ contracts
            region: Region code
            ktru: KTRU code
            date_from: Start date
            date_to: End date
            max_pages: Maximum number of pages to fetch
            
        Returns:
            SearchResult object with all cards from all pages
        """
        all_cards = []
        total_count = 0
        
        for page in range(1, max_pages + 1):
            url = self.build_search_url(
                fz_44=fz_44,
                region=region,
                ktru=ktru,
                date_from=date_from,
                date_to=date_to,
                page=page
            )
            
            try:
                html = self.fetch_search_page(url)
                result = self.parse_list(html)
                
                if page == 1:
                    total_count = result.total_count
                
                all_cards.extend(result.cards)
                
                # Stop if we've fetched all cards or if there are no more cards
                if not result.cards or len(all_cards) >= total_count:
                    break
                    
            except Exception as e:
                print(f"Error fetching page {page}: {e}")
                break
        
        return SearchResult(
            total_count=total_count,
            cards=all_cards
        )