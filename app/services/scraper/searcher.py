"""
Zakupki Searcher - Scraper for Russian procurement website.
Implements search functionality for contracts with URL construction,
HTML parsing, and result extraction.
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlencode

import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field


class SearchParams(BaseModel):
    """Parameters for searching contracts on zakupki.gov.ru"""
    law_type: str = Field(default="44-FZ", description="Type of law (44-FZ, 223-FZ, etc.)")
    region: Optional[str] = Field(default=None, description="Region code")
    date_from: Optional[str] = Field(default=None, description="Start date in format DD.MM.YYYY")
    date_to: Optional[str] = Field(default=None, description="End date in format DD.MM.YYYY")
    ktru: Optional[str] = Field(default=None, description="KTRU code")
    page: int = Field(default=1, ge=1, description="Page number")
    limit_contracts: Optional[int] = Field(default=None, ge=1, description="Maximum number of contracts to fetch")


class ContractInfo(BaseModel):
    """Information about a single contract."""
    reestr_number: str = Field(..., description="Registry number of the contract")
    date: Optional[datetime] = Field(None, description="Contract date")
    price: Optional[float] = Field(None, ge=0, description="Contract price")
    link: Optional[str] = Field(None, description="Link to contract details")


class SearchResult(BaseModel):
    """Result of a search operation."""
    found_total: int = Field(..., ge=0, description="Total number of contracts found")
    contracts: List[ContractInfo] = Field(default_factory=list, description="List of contracts")
    has_more: bool = Field(default=False, description="Whether there are more pages to fetch")


class ZakupkiSearcher:
    """Searcher for zakupki.gov.ru website."""
    
    BASE_URL = "https://zakupki.gov.ru"
    SEARCH_URL = f"{BASE_URL}/epz/order/extendedsearch/results.html"
    
    # Rotating user agents to avoid blocking
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    ]
    
    def __init__(self, timeout: float = 30.0, max_retries: int = 3):
        """
        Initialize the searcher.
        
        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self._client = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            timeout=self.timeout,
            follow_redirects=True,
            headers={"User-Agent": random.choice(self.USER_AGENTS)}
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()
            
    def _build_search_url(self, params: SearchParams) -> str:
        """
        Build search URL from parameters.
        
        Args:
            params: Search parameters
            
        Returns:
            Complete search URL
        """
        query_params = {
            "searchString": "",
            "morphology": "on",
            "searchFilter": params.law_type,
            "pageNumber": params.page,
            "sortDirection": "false",
            "recordsPerPage": "_50",
            "showLotsInfoHidden": "false",
            "sortBy": "UPDATE_DATE",
            "fz44": "on" if params.law_type == "44-FZ" else "off",
            "fz223": "on" if params.law_type == "223-FZ" else "off",
            "af": "on",
            "ca": "on",
            "pc": "on",
            "pa": "on",
        }
        
        # Add optional parameters
        if params.region:
            query_params["regions"] = params.region
            
        if params.date_from:
            query_params["publishDateFrom"] = params.date_from
            
        if params.date_to:
            query_params["publishDateTo"] = params.date_to
            
        if params.ktru:
            query_params["ktru"] = params.ktru
            
        return f"{self.SEARCH_URL}?{urlencode(query_params)}"
    
    def _parse_found_total(self, soup: BeautifulSoup) -> int:
        """
        Parse total number of found records from HTML.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Total number of records found
        """
        # Look for text like "Found X records"
        found_text_elements = soup.find_all(string=lambda text: text and "Found" in text and "records" in text)
        
        for element in found_text_elements:
            text = element.strip()
            # Extract number from text like "Found 1234 records"
            import re
            match = re.search(r'Found\s+([\d,]+)\s+records', text)
            if match:
                # Remove commas from number
                number_str = match.group(1).replace(',', '')
                return int(number_str)
                
        return 0
    
    def _parse_contracts(self, soup: BeautifulSoup) -> List[ContractInfo]:
        """
        Parse contract list from HTML.
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            List of contract information
        """
        contracts = []
        
        # Find contract rows - this selector may need adjustment based on actual HTML structure
        contract_rows = soup.select(".search-registry-entry-block")
        
        for row in contract_rows:
            try:
                # Extract reestr number
                reestr_elem = row.select_one(".registry-entry__header-mid__number a")
                reestr_number = reestr_elem.text.strip() if reestr_elem else ""
                
                # Extract link
                link = None
                if reestr_elem and reestr_elem.get('href'):
                    link = f"{self.BASE_URL}{reestr_elem['href']}"
                
                # Extract date
                date_elem = row.select_one(".data-block__value")
                date_str = date_elem.text.strip() if date_elem else None
                date = None
                if date_str:
                    try:
                        date = datetime.strptime(date_str, "%d.%m.%Y")
                    except ValueError:
                        pass
                
                # Extract price
                price_elem = row.select_one(".price-block__value")
                price = None
                if price_elem:
                    price_text = price_elem.text.strip()
                    # Remove currency symbol and spaces, convert to float
                    import re
                    match = re.search(r'([\d\s,]+)', price_text)
                    if match:
                        price_str = match.group(1).replace(' ', '').replace(',', '.')
                        try:
                            price = float(price_str)
                        except ValueError:
                            pass
                
                if reestr_number:
                    contracts.append(ContractInfo(
                        reestr_number=reestr_number,
                        date=date,
                        price=price,
                        link=link
                    ))
                    
            except Exception as e:
                # Skip malformed rows but continue processing
                continue
                
        return contracts
    
    async def search(self, params: SearchParams, stop_event: Optional[asyncio.Event] = None) -> SearchResult:
        """
        Search for contracts with given parameters.
        
        Args:
            params: Search parameters
            stop_event: Optional event to signal stopping the search
            
        Returns:
            Search result with contracts
        """
        if not self._client:
            raise RuntimeError("Searcher must be used as async context manager")
            
        contracts = []
        found_total = 0
        current_page = params.page
        has_more = True
        
        while has_more:
            # Check if we should stop
            if stop_event and stop_event.is_set():
                break
                
            # Check limit
            if params.limit_contracts and len(contracts) >= params.limit_contracts:
                break
                
            # Build URL for current page
            page_params = params.model_copy(update={"page": current_page})
            url = self._build_search_url(page_params)
            
            # Make request with retries
            response = None
            for attempt in range(self.max_retries):
                try:
                    # Rotate user agent
                    headers = {"User-Agent": random.choice(self.USER_AGENTS)}
                    response = await self._client.get(url, headers=headers)
                    response.raise_for_status()
                    break
                except (httpx.RequestError, httpx.HTTPStatusError) as e:
                    if attempt == self.max_retries - 1:
                        raise
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'lxml')
            
            # Parse total count (only on first page)
            if current_page == params.page:
                found_total = self._parse_found_total(soup)
            
            # Parse contracts
            page_contracts = self._parse_contracts(soup)
            
            # Add contracts up to limit
            if params.limit_contracts:
                remaining = params.limit_contracts - len(contracts)
                contracts.extend(page_contracts[:remaining])
            else:
                contracts.extend(page_contracts)
            
            # Check if there are more pages
            has_more = bool(page_contracts) and (
                not params.limit_contracts or len(contracts) < params.limit_contracts
            )
            
            # Move to next page
            current_page += 1
            
            # Small delay between requests to be polite
            await asyncio.sleep(random.uniform(1.0, 2.0))
        
        return SearchResult(
            found_total=found_total,
            contracts=contracts,
            has_more=has_more and (not params.limit_contracts or len(contracts) < found_total)
        )