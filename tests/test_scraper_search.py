"""
Tests for ZakupkiSearcher scraper.
"""

import asyncio
from datetime import datetime
from pathlib import Path

import pytest
import respx
import httpx
from httpx import Response

from app.services.scraper.searcher import ZakupkiSearcher, SearchParams, ContractInfo


# Fixture for loading HTML test data
@pytest.fixture
def search_results_html():
    """Load HTML fixture for testing."""
    fixture_path = Path(__file__).parent / "fixtures" / "search_results.html"
    return fixture_path.read_text(encoding="utf-8")


@pytest.fixture
def mock_search_response(search_results_html):
    """Mock HTTP response for search requests."""
    with respx.mock:
        # Mock the search endpoint
        respx.get("https://zakupki.gov.ru/epz/order/extendedsearch/results.html").mock(
            return_value=Response(
                status_code=200,
                text=search_results_html,
                headers={"Content-Type": "text/html"}
            )
        )
        yield


class TestZakupkiSearcher:
    """Test suite for ZakupkiSearcher."""
    
    def test_build_search_url_default(self):
        """Test URL construction with default parameters."""
        searcher = ZakupkiSearcher()
        params = SearchParams(law_type="44-FZ", page=1)
        
        url = searcher._build_search_url(params)
        
        assert "https://zakupki.gov.ru/epz/order/extendedsearch/results.html?" in url
        assert "searchFilter=44-FZ" in url
        assert "pageNumber=1" in url
        assert "fz44=on" in url
        assert "fz223=off" in url
        
    def test_build_search_url_with_all_params(self):
        """Test URL construction with all parameters."""
        searcher = ZakupkiSearcher()
        params = SearchParams(
            law_type="223-FZ",
            region="77",  # Moscow
            date_from="01.01.2024",
            date_to="31.01.2024",
            ktru="31.20.11.110",
            page=2
        )
        
        url = searcher._build_search_url(params)
        
        assert "searchFilter=223-FZ" in url
        assert "regions=77" in url
        assert "publishDateFrom=01.01.2024" in url
        assert "publishDateTo=31.01.2024" in url
        assert "ktru=31.20.11.110" in url
        assert "pageNumber=2" in url
        assert "fz223=on" in url
        
    def test_parse_found_total(self, search_results_html):
        """Test parsing total number of found records."""
        from bs4 import BeautifulSoup
        
        searcher = ZakupkiSearcher()
        soup = BeautifulSoup(search_results_html, 'lxml')
        
        found_total = searcher._parse_found_total(soup)
        
        assert found_total == 1234
        
    def test_parse_contracts(self, search_results_html):
        """Test parsing contract list from HTML."""
        from bs4 import BeautifulSoup
        
        searcher = ZakupkiSearcher()
        soup = BeautifulSoup(search_results_html, 'lxml')
        
        contracts = searcher._parse_contracts(soup)
        
        # Should find 5 contracts
        assert len(contracts) == 5
        
        # Check first contract
        contract1 = contracts[0]
        assert contract1.reestr_number == "12345678901234567890"
        assert contract1.date == datetime(2024, 1, 15)
        assert contract1.price == 1234567.89
        assert contract1.link == "https://zakupki.gov.ru/epz/order/notice/ea44/view/common-info.html?regNumber=12345678901234567890"
        
        # Check second contract
        contract2 = contracts[1]
        assert contract2.reestr_number == "09876543210987654321"
        assert contract2.date == datetime(2024, 1, 20)
        assert contract2.price == 987654.32
        
        # Check third contract
        contract3 = contracts[2]
        assert contract3.reestr_number == "11223344556677889900"
        assert contract3.date == datetime(2024, 1, 25)
        assert contract3.price == 555555.55
        
    @pytest.mark.asyncio
    async def test_search_single_page(self, mock_search_response):
        """Test search with single page of results."""
        async with ZakupkiSearcher() as searcher:
            params = SearchParams(
                law_type="44-FZ",
                page=1
            )
            
            result = await searcher.search(params)
            
            # Check total count
            assert result.found_total == 1234
            
            # Check contracts
            assert len(result.contracts) == 5
            assert result.has_more == True  # There are more pages available
            
            # Verify contract data
            contract = result.contracts[0]
            assert isinstance(contract, ContractInfo)
            assert contract.reestr_number == "12345678901234567890"
            
    @pytest.mark.asyncio
    async def test_search_with_limit(self, mock_search_response):
        """Test search with contract limit."""
        async with ZakupkiSearcher() as searcher:
            params = SearchParams(
                law_type="44-FZ",
                page=1,
                limit_contracts=2
            )
            
            result = await searcher.search(params)
            
            # Should only get 2 contracts due to limit
            assert len(result.contracts) == 2
            assert result.contracts[0].reestr_number == "12345678901234567890"
            assert result.contracts[1].reestr_number == "09876543210987654321"
            
    @pytest.mark.asyncio
    async def test_search_with_stop_event(self, mock_search_response):
        """Test search with stop event."""
        async with ZakupkiSearcher() as searcher:
            params = SearchParams(
                law_type="44-FZ",
                page=1
            )
            
            # Create stop event and set it immediately
            stop_event = asyncio.Event()
            stop_event.set()
            
            result = await searcher.search(params, stop_event)
            
            # Should get empty result because stopped immediately
            assert len(result.contracts) == 0
            
    @pytest.mark.asyncio
    async def test_search_error_handling(self):
        """Test search error handling with retries."""
        with respx.mock:
            # Mock server error
            respx.get("https://zakupki.gov.ru/epz/order/extendedsearch/results.html").mock(
                return_value=Response(status_code=500)
            )
            
            async with ZakupkiSearcher(max_retries=2) as searcher:
                params = SearchParams(law_type="44-FZ", page=1)
                
                # Should raise after retries
                with pytest.raises(Exception):
                    await searcher.search(params)
                    
    def test_contract_info_model(self):
        """Test ContractInfo Pydantic model."""
        contract = ContractInfo(
            reestr_number="1234567890",
            date=datetime(2024, 1, 15),
            price=1000.50,
            link="https://example.com/contract"
        )
        
        assert contract.reestr_number == "1234567890"
        assert contract.date.year == 2024
        assert contract.price == 1000.50
        assert contract.link == "https://example.com/contract"
        
    def test_search_params_model(self):
        """Test SearchParams Pydantic model."""
        params = SearchParams(
            law_type="44-FZ",
            region="77",
            date_from="01.01.2024",
            date_to="31.01.2024",
            ktru="31.20.11.110",
            page=1,
            limit_contracts=100
        )
        
        assert params.law_type == "44-FZ"
        assert params.region == "77"
        assert params.date_from == "01.01.2024"
        assert params.date_to == "31.01.2024"
        assert params.ktru == "31.20.11.110"
        assert params.page == 1
        assert params.limit_contracts == 100
        
    @pytest.mark.asyncio
    async def test_context_manager(self):
        """Test async context manager functionality."""
        async with ZakupkiSearcher() as searcher:
            assert searcher._client is not None
            assert isinstance(searcher._client, httpx.AsyncClient)
            
        # Client should be closed after context exit
        assert searcher._client is None or searcher._client.is_closed