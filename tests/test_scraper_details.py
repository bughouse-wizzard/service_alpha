import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.scraper.parser import ContractParser, parse_card


class TestContractParser:
    """Test suite for ContractParser class."""
    
    @pytest.fixture
    def mock_client(self):
        """Create a mock HTTP client."""
        client = AsyncMock()
        client.get = AsyncMock()
        client.head = AsyncMock()
        client.aclose = AsyncMock()
        return client
    
    @pytest.fixture
    def parser(self, mock_client):
        """Create parser with mock client."""
        return ContractParser(client=mock_client)
    
    @pytest.fixture
    def common_info_html(self):
        """Mock common-info.html content."""
        return """
        <html>
            <body>
                <table>
                    <tr>
                        <td>Дата</td>
                        <td>2025-01-15</td>
                    </tr>
                    <tr>
                        <td>Заказчик</td>
                        <td>Министерство цифрового развития</td>
                    </tr>
                    <tr>
                        <td>Другие данные</td>
                        <td>Неважно</td>
                    </tr>
                </table>
                <a href="objects.html">Позиции и объекты</a>
                <a href="attachments.html">Документы</a>
            </body>
        </html>
        """
    
    @pytest.fixture
    def objects_html(self):
        """Mock objects.html content with table."""
        return """
        <html>
            <body>
                <table>
                    <tr>
                        <th>Позиция</th>
                        <th>КТРУ</th>
                        <th>Цена за единицу</th>
                    </tr>
                    <tr>
                        <td>Разработка ПО</td>
                        <td>1234567890</td>
                        <td>1 500 000,00 руб.</td>
                    </tr>
                    <tr>
                        <td>Тестирование</td>
                        <td>0987654321</td>
                        <td>750 000,50 руб.</td>
                    </tr>
                </table>
            </body>
        </html>
        """
    
    @pytest.fixture
    def attachments_html(self):
        """Mock attachments.html content."""
        return """
        <html>
            <body>
                <h3>Документы по контракту 2025-001</h3>
                <ul>
                    <li><a href="/files/contract_2025.pdf">Печатная форма договора 2025</a></li>
                    <li><a href="/files/spec_2025.pdf">Спецификация 2025</a></li>
                    <li><a href="/files/old_2020.pdf">Договор 2020</a></li>
                </ul>
            </body>
        </html>
        """
    
    @pytest.mark.asyncio
    async def test_parse_common_info(self, parser, common_info_html):
        """Test parsing date and customer from common-info.html."""
        result = parser._parse_common_info(common_info_html)
        
        assert result["date"] == "2025-01-15"
        assert result["customer"] == "Министерство цифрового развития"
    
    @pytest.mark.asyncio
    async def test_parse_objects_table(self, parser, objects_html):
        """Test parsing positions table from objects.html."""
        positions = parser._parse_objects_table(objects_html)
        
        assert len(positions) == 2
        
        # Check first position
        assert positions[0]["position"] == "Разработка ПО"
        assert positions[0]["ktru"] == "1234567890"
        assert positions[0]["unit_price"] == "1500000.00"  # Cleaned price
        
        # Check second position
        assert positions[1]["position"] == "Тестирование"
        assert positions[1]["ktru"] == "0987654321"
        assert positions[1]["unit_price"] == "750000.50"  # Cleaned price
    
    @pytest.mark.asyncio
    async def test_find_objects_url_from_html(self, parser, mock_client, common_info_html):
        """Test finding objects URL from common-info.html."""
        base_url = "https://example.com/contract/123/"
        
        # Mock head responses for URL checking
        mock_client.head.return_value.status_code = 404
        
        url = await parser._find_objects_url(base_url, common_info_html)
        
        assert url == "https://example.com/contract/123/objects.html"
    
    @pytest.mark.asyncio
    async def test_find_objects_url_pattern(self, parser, mock_client):
        """Test finding objects URL using pattern matching."""
        base_url = "https://example.com/contract/123/"
        
        # Mock head to return 200 for objects.html
        mock_response = MagicMock()
        mock_response.status_code = 200
        
        def side_effect(url):
            if "objects.html" in url:
                return mock_response
            mock_response.status_code = 404
            return mock_response
        
        mock_client.head.side_effect = side_effect
        
        url = await parser._find_objects_url(base_url)
        
        assert url == "https://example.com/contract/123/objects.html"
    
    @pytest.mark.asyncio
    async def test_parse_card_full_flow(self, parser, mock_client, common_info_html, objects_html, attachments_html):
        """Test full parse_card flow with mocked responses."""
        base_url = "https://example.com/contract/123/"
        
        # Mock responses
        mock_client.get.side_effect = [
            # common-info.html
            MagicMock(text=common_info_html, status_code=200),
            # objects.html
            MagicMock(text=objects_html, status_code=200),
            # attachments.html
            MagicMock(text=attachments_html, status_code=200),
            # file download (contract_2025.pdf)
            MagicMock(content=b"PDF_CONTENT", status_code=200),
        ]
        
        # Mock head for URL discovery
        mock_head_response = MagicMock()
        mock_head_response.status_code = 200
        mock_client.head.return_value = mock_head_response
        
        result = await parser.parse_card(base_url)
        
        # Verify basic structure
        assert result["url"] == base_url
        assert result["date"] == "2025-01-15"
        assert result["customer"] == "Министерство цифрового развития"
        
        # Verify positions
        assert len(result["positions"]) == 2
        assert result["positions"][0]["position"] == "Разработка ПО"
        assert result["positions"][0]["unit_price"] == "1500000.00"
        
        # Verify attachments (should find 2025+ files)
        # Should find at least the 2025 contract
        assert len(result["attachments"]) >= 1
        if result["attachments"]:
            assert "2025" in result["attachments"][0]["name"].lower() or "печатная" in result["attachments"][0]["name"].lower()
    
    @pytest.mark.asyncio
    async def test_parse_card_error_handling(self, parser, mock_client):
        """Test error handling in parse_card."""
        base_url = "https://example.com/contract/123/"
        
        # Mock all requests to fail
        mock_client.get.side_effect = Exception("Network error")
        mock_client.head.side_effect = Exception("Network error")
        
        result = await parser.parse_card(base_url)
        
        # Should return empty result structure (errors are caught internally)
        assert result["url"] == base_url
        assert result["date"] is None
        assert result["customer"] is None
        assert result["positions"] == []
        assert result["attachments"] == []
        # Check that error was stored internally
        assert parser.last_error == "Network error"
    
    @pytest.mark.asyncio
    async def test_download_file_success(self, parser, mock_client):
        """Test successful file download."""
        file_url = "https://example.com/file.pdf"
        mock_content = b"PDF_FILE_CONTENT"
        
        mock_response = MagicMock()
        mock_response.content = mock_content
        mock_response.raise_for_status = MagicMock()
        
        mock_client.get.return_value = mock_response
        
        content = await parser._download_file(file_url)
        
        assert content == mock_content
        mock_client.get.assert_called_once_with(file_url)
    
    @pytest.mark.asyncio
    async def test_download_file_failure(self, parser, mock_client):
        """Test file download failure."""
        file_url = "https://example.com/file.pdf"
        
        mock_client.get.side_effect = Exception("Download failed")
        
        content = await parser._download_file(file_url)
        
        assert content is None
    
    def test_get_common_info_url(self, parser):
        """Test URL construction for common-info.html."""
        base_url = "https://example.com/contract/123/page.html"
        expected = "https://example.com/contract/123/common-info.html"
        
        result = parser._get_common_info_url(base_url)
        
        assert result == expected


@pytest.mark.asyncio
async def test_parse_card_convenience_function():
    """Test the convenience parse_card function."""
    with patch('app.services.scraper.parser.ContractParser') as MockParser:
        mock_parser = AsyncMock()
        mock_parser.parse_card = AsyncMock(return_value={"test": "data"})
        mock_parser.close = AsyncMock()
        MockParser.return_value = mock_parser
        
        result = await parse_card("https://example.com")
        
        assert result == {"test": "data"}
        mock_parser.close.assert_called_once()