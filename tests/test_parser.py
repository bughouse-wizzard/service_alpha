"""
Tests for ZakupkiSearcher parser.
"""

import os
from datetime import date
from pathlib import Path

import pytest

from app.services.zakupki_parser import ZakupkiSearcher, ContractCard, SearchResult


@pytest.fixture
def sample_html():
    """Load sample HTML fixture."""
    fixture_path = Path(__file__).parent / "fixtures" / "search_results.html"
    return fixture_path.read_text(encoding="utf-8")


@pytest.fixture
def searcher():
    """Create ZakupkiSearcher instance."""
    return ZakupkiSearcher()


class TestZakupkiSearcher:
    """Test ZakupkiSearcher class."""
    
    def test_parse_total_count(self, searcher, sample_html):
        """Test parsing total count from HTML."""
        total_count = searcher.parse_total_count(sample_html)
        assert total_count == 125
    
    def test_parse_contract_cards(self, searcher, sample_html):
        """Test parsing contract cards from HTML."""
        cards = searcher.parse_contract_cards(sample_html)
        
        # Should find 5 cards in the sample HTML
        assert len(cards) == 5
        
        # Check first card
        first_card = cards[0]
        assert isinstance(first_card, ContractCard)
        assert first_card.reestr_number == "0373200001424000001"
        assert first_card.contract_date == date(2024, 1, 15)
        assert first_card.price == 1250000.50
        assert first_card.link == "https://zakupki.gov.ru/epz/contract/contractCard/document-info.html?reestrNumber=0373200001424000001"
        assert first_card.title == "Поставка компьютерной техники для государственных нужд"
        
        # Check second card
        second_card = cards[1]
        assert second_card.reestr_number == "0373200001424000002"
        assert second_card.contract_date == date(2024, 1, 20)
        assert second_card.price == 850000.00
        assert second_card.link == "https://zakupki.gov.ru/epz/contract/contractCard/document-info.html?reestrNumber=0373200001424000002"
        assert second_card.title == "Ремонт административного здания"
    
    def test_parse_list(self, searcher, sample_html):
        """Test parse_list method returns SearchResult with correct data."""
        result = searcher.parse_list(sample_html)
        
        assert isinstance(result, SearchResult)
        assert result.total_count == 125
        assert len(result.cards) == 5
        
        # Verify all cards are ContractCard instances
        for card in result.cards:
            assert isinstance(card, ContractCard)
        
        # Verify specific card data
        card_numbers = [card.reestr_number for card in result.cards]
        expected_numbers = [
            "0373200001424000001",
            "0373200001424000002", 
            "0373200001424000003",
            "0373200001424000004",
            "0373200001424000005"
        ]
        assert card_numbers == expected_numbers
    
    def test_build_search_url_default(self, searcher):
        """Test URL construction with default parameters."""
        url = searcher.build_search_url()
        
        assert url.startswith("https://zakupki.gov.ru/epz/contract/search/results.html?")
        assert "pageNumber=1" in url
        assert "fz44=on" in url
        assert "af=on" in url
        assert "sortDirection=false" in url
        assert "recordsPerPage=_50" in url
    
    def test_build_search_url_with_params(self, searcher):
        """Test URL construction with custom parameters."""
        url = searcher.build_search_url(
            fz_44=True,
            region="77",
            ktru="31.20.11.110",
            date_from=date(2024, 1, 1),
            date_to=date(2024, 1, 31),
            page=2
        )
        
        assert "regions=77" in url
        assert "ktru=31.20.11.110" in url
        assert "contractDateFrom=01.01.2024" in url
        assert "contractDateTo=31.01.2024" in url
        assert "pageNumber=2" in url
    
    def test_build_search_url_fz_44_false(self, searcher):
        """Test URL construction with fz_44=False."""
        url = searcher.build_search_url(fz_44=False)
        assert "fz44=off" in url
    
    def test_contract_card_dataclass(self):
        """Test ContractCard dataclass."""
        card = ContractCard(
            reestr_number="0373200001424000001",
            contract_date=date(2024, 1, 15),
            price=1250000.50,
            link="https://example.com",
            title="Test Contract",
            customer="Test Customer",
            supplier="Test Supplier"
        )
        
        assert card.reestr_number == "0373200001424000001"
        assert card.contract_date == date(2024, 1, 15)
        assert card.price == 1250000.50
        assert card.link == "https://example.com"
        assert card.title == "Test Contract"
        assert card.customer == "Test Customer"
        assert card.supplier == "Test Supplier"
    
    def test_search_result_dataclass(self):
        """Test SearchResult dataclass."""
        cards = [
            ContractCard(
                reestr_number="001",
                contract_date=date(2024, 1, 1),
                price=1000.0,
                link="https://example.com/1"
            ),
            ContractCard(
                reestr_number="002",
                contract_date=date(2024, 1, 2),
                price=2000.0,
                link="https://example.com/2"
            )
        ]
        
        result = SearchResult(total_count=100, cards=cards)
        
        assert result.total_count == 100
        assert len(result.cards) == 2
        assert result.cards[0].reestr_number == "001"
        assert result.cards[1].reestr_number == "002"
    
    def test_parse_empty_html(self, searcher):
        """Test parsing empty HTML."""
        empty_html = "<html><body></body></html>"
        result = searcher.parse_list(empty_html)
        
        assert result.total_count == 0
        assert len(result.cards) == 0
    
    def test_parse_html_with_no_count(self, searcher):
        """Test parsing HTML without count information."""
        html_without_count = "<html><body><div>Some content</div></body></html>"
        total_count = searcher.parse_total_count(html_without_count)
        
        assert total_count == 0
    
    def test_parse_html_with_different_count_format(self, searcher):
        """Test parsing HTML with different count formats."""
        # Test with non-breaking space
        html1 = '<div class="search-results__count">125&nbsp;записей</div>'
        assert searcher.parse_total_count(html1) == 125
        
        # Test with regular space
        html2 = '<div class="search-results__count">125 записей</div>'
        assert searcher.parse_total_count(html2) == 125
        
        # Test with thousands separator
        html3 = '<div class="search-results__count">1 250 записей</div>'
        assert searcher.parse_total_count(html3) == 1250
        
        # Test with different wording
        html4 = '<div class="search-results__count">42 записи</div>'
        assert searcher.parse_total_count(html4) == 42