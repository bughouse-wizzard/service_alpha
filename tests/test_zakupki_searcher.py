import uuid
import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

from app.services.zakupki_searcher import ZakupkiSearcher


class TestZakupkiSearcher:
    """Test suite for ZakupkiSearcher"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.search_id = uuid.uuid4()
        self.searcher = ZakupkiSearcher(self.search_id)
        self.reestr_number = "1234567890"
        self.ktru_code = "12345678"
    
    def teardown_method(self):
        """Cleanup after tests"""
        if hasattr(self, 'searcher'):
            self.searcher.close()
    
    @patch('app.services.zakupki_searcher.httpx.Client')
    def test_fetch_contract_card_success(self, mock_client_class):
        """Test successful contract card fetch"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <span>Заказчик</span>
                <span class="cardMainInfo__content">Test Customer Inc.</span>
                <span>Дата размещения</span>
                <span class="cardMainInfo__content">2024-01-15</span>
                <span>Дата обновления</span>
                <span class="cardMainInfo__content">2024-01-20</span>
            </body>
        </html>
        """
        
        # Mock client
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        # Replace client
        self.searcher.client = mock_client
        
        # Test
        result = self.searcher.fetch_contract_card(self.reestr_number)
        
        # Verify
        assert result['reestr_number'] == self.reestr_number
        assert result['customer_name'] == 'Test Customer Inc.'
        assert result['publication_date'] == '2024-01-15'
        assert result['update_date'] == '2024-01-20'
        assert 'common_info_html' in result
        
        # Verify URL was called correctly
        expected_url = f"https://zakupki.gov.ru/epz/order/notice/ea44/view/common-info.html?regNumber={self.reestr_number}"
        mock_client.get.assert_called_once_with(expected_url)
    
    @patch('app.services.zakupki_searcher.httpx.Client')
    def test_fetch_contract_card_failure(self, mock_client_class):
        """Test contract card fetch failure"""
        # Mock response with error
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("Not found")
        
        # Mock client
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        # Replace client
        self.searcher.client = mock_client
        
        # Test
        with pytest.raises(Exception, match="Error parsing contract card"):
            self.searcher.fetch_contract_card(self.reestr_number)
    
    @patch('app.services.zakupki_searcher.httpx.Client')
    def test_fetch_contract_objects_success(self, mock_client_class):
        """Test successful contract objects fetch"""
        # Mock responses for multiple URL attempts
        mock_response1 = Mock()
        mock_response1.status_code = 404
        
        mock_response2 = Mock()
        mock_response2.status_code = 200
        mock_response2.text = """
        <html>
            <body>
                <table>
                    <tr><th>КТРУ</th><th>наименование</th><th>Цена за единицу</th></tr>
                    <tr><td>12345678</td><td>Test Product</td><td>1000.50</td></tr>
                    <tr><td>87654321</td><td>Another Product</td><td>2000.00</td></tr>
                </table>
            </body>
        </html>
        """
        
        # Mock client
        mock_client = Mock()
        mock_client.get.side_effect = [mock_response1, mock_response2]
        mock_client_class.return_value = mock_client
        
        # Replace client
        self.searcher.client = mock_client
        
        # Test
        result = self.searcher.fetch_contract_objects(self.reestr_number, self.ktru_code)
        
        # Verify
        assert result['objects_url'] is not None
        assert result['ktru_found'] is True
        assert result['unit_price'] == 1000.50  # pandas returns float
        assert result['specification_text'] == 'Test Product'
        assert len(result['objects']) > 0
        assert 'objects_html' in result
    
    @patch('app.services.zakupki_searcher.httpx.Client')
    def test_fetch_contract_objects_no_ktru_match(self, mock_client_class):
        """Test contract objects fetch with no KTRU match"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <table>
                    <tr><th>КТРУ</th><th>Наименование</th><th>Цена за единицу</th></tr>
                    <tr><td>99999999</td><td>Different Product</td><td>500.00</td></tr>
                </table>
            </body>
        </html>
        """
        
        # Mock client
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        # Replace client
        self.searcher.client = mock_client
        
        # Test
        result = self.searcher.fetch_contract_objects(self.reestr_number, self.ktru_code)
        
        # Verify
        assert result['ktru_found'] is False
        assert result['unit_price'] is None
        assert result['specification_text'] is None
    
    @patch('app.services.zakupki_searcher.httpx.Client')
    def test_fetch_attachments(self, mock_client_class):
        """Test fetching attachments"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
        <html>
            <body>
                <a href="/documents/test.pdf">test.pdf</a>
                <a href="/documents/spec.docx">Спецификация.docx</a>
                <a href="/print-form">Печатная форма</a>
                <a href="http://external.com/doc.pdf">External PDF</a>
            </body>
        </html>
        """
        
        # Mock client
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        # Replace client
        self.searcher.client = mock_client
        
        # Test
        attachments = self.searcher.fetch_attachments(self.reestr_number)
        
        # Verify
        assert len(attachments) == 4
        
        # Check PDF attachment
        pdf_attachments = [a for a in attachments if a['type'] == 'pdf']
        assert len(pdf_attachments) >= 1
        
        # Check DOCX attachment
        docx_attachments = [a for a in attachments if a['type'] == 'docx']
        assert len(docx_attachments) >= 1
        
        # Check print form
        print_forms = [a for a in attachments if a['type'] == 'print_form']
        assert len(print_forms) >= 1
    
    @patch('app.services.zakupki_searcher.httpx.Client')
    def test_download_attachment(self, mock_client_class, tmp_path):
        """Test downloading an attachment"""
        # Create temporary storage directory
        storage_dir = tmp_path / "storage"
        self.searcher.storage_base = storage_dir
        
        # Mock attachment
        attachment = {
            'name': 'test.pdf',
            'url': 'https://zakupki.gov.ru/documents/test.pdf',
            'type': 'pdf'
        }
        
        # Mock response with PDF content
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b'%PDF-1.4 test pdf content'
        
        # Mock client
        mock_client = Mock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client
        
        # Replace client
        self.searcher.client = mock_client
        
        # Test
        filepath = self.searcher.download_attachment(attachment, self.reestr_number)
        
        # Verify
        assert filepath is not None
        assert Path(filepath).exists()
        assert Path(filepath).name == 'test.pdf'
        
        # Check directory structure
        contract_dir = storage_dir / str(self.search_id) / self.reestr_number
        assert contract_dir.exists()
    
    def test_is_recent_contract(self):
        """Test recent contract detection"""
        # Test 2024 contract (not recent)
        contract_2024 = {
            'publication_date': '2024-01-15',
            'contract_date': '2024-02-01'
        }
        assert self.searcher._is_recent_contract(contract_2024) is False
        
        # Test 2025 contract (recent)
        contract_2025 = {
            'publication_date': '2025-01-15'
        }
        assert self.searcher._is_recent_contract(contract_2025) is True
        
        # Test 2026 contract (recent)
        contract_2026 = {
            'update_date': '2026-01-01'
        }
        assert self.searcher._is_recent_contract(contract_2026) is True
        
        # Test no date (not recent)
        contract_no_date = {}
        assert self.searcher._is_recent_contract(contract_no_date) is False
    
    def test_sanitize_filename(self):
        """Test filename sanitization"""
        # Test normal filename
        assert self.searcher._sanitize_filename("test.pdf") == "test.pdf"
        
        # Test filename with invalid characters
        assert self.searcher._sanitize_filename("test<>.pdf") == "test__.pdf"
        
        # Test very long filename
        long_name = "a" * 300 + ".pdf"
        sanitized = self.searcher._sanitize_filename(long_name)
        assert len(sanitized) <= 200
        assert sanitized.endswith(".pdf")
        
        # Test empty filename
        assert self.searcher._sanitize_filename("") == ""
    
    @patch.object(ZakupkiSearcher, 'fetch_contract_card')
    @patch.object(ZakupkiSearcher, 'fetch_contract_objects')
    @patch.object(ZakupkiSearcher, 'fetch_attachments')
    @patch.object(ZakupkiSearcher, 'download_attachment')
    def test_parse_contract_details_success(self, mock_download, mock_fetch_attachments, 
                                           mock_fetch_objects, mock_fetch_card):
        """Test successful contract details parsing"""
        # Mock contract card
        mock_fetch_card.return_value = {
            'customer_name': 'Test Customer',
            'publication_date': '2024-01-15',
            'reestr_number': self.reestr_number
        }
        
        # Mock objects
        mock_fetch_objects.return_value = {
            'unit_price': '1500.75',
            'specification_text': 'Test Product Specification',
            'ktru_found': True,
            'objects': [{'КТРУ': self.ktru_code, 'Наименование': 'Test Product'}]
        }
        
        # Mock attachments
        mock_fetch_attachments.return_value = []
        mock_download.return_value = None
        
        # Test
        result = self.searcher.parse_contract_details(self.reestr_number, self.ktru_code)
        
        # Verify
        assert result['success'] is True
        assert result['error'] is None
        assert result['contract_card'] is not None
        assert result['objects'] is not None
        assert result['warnings'] == []  # No warnings when everything is found
    
    @patch.object(ZakupkiSearcher, 'fetch_contract_card')
    @patch.object(ZakupkiSearcher, 'fetch_contract_objects')
    @patch.object(ZakupkiSearcher, 'fetch_attachments')
    @patch.object(ZakupkiSearcher, 'download_attachment')
    def test_parse_contract_details_price_not_found(self, mock_download, mock_fetch_attachments,
                                                   mock_fetch_objects, mock_fetch_card):
        """Test contract details parsing with price not found"""
        # Mock contract card
        mock_fetch_card.return_value = {
            'customer_name': 'Test Customer',
            'publication_date': '2024-01-15',
            'reestr_number': self.reestr_number
        }
        
        # Mock objects without price
        mock_fetch_objects.return_value = {
            'unit_price': None,
            'specification_text': 'Test Product Specification',
            'ktru_found': True,
            'objects': [{'КТРУ': self.ktru_code, 'Наименование': 'Test Product'}]
        }
        
        # Mock attachments
        mock_fetch_attachments.return_value = []
        mock_download.return_value = None
        
        # Test
        result = self.searcher.parse_contract_details(self.reestr_number, self.ktru_code)
        
        # Verify
        assert result['success'] is True
        assert 'Price not found in objects table' in result['warnings']
    
    @patch.object(ZakupkiSearcher, 'fetch_contract_card')
    @patch.object(ZakupkiSearcher, 'fetch_contract_objects')
    def test_parse_contract_details_failure(self, mock_fetch_objects, mock_fetch_card):
        """Test contract details parsing failure"""
        # Mock failure
        mock_fetch_card.side_effect = Exception("Network error")
        
        # Test
        result = self.searcher.parse_contract_details(self.reestr_number, self.ktru_code)
        
        # Verify
        assert result['success'] is False
        assert result['error'] == 'Network error'
        assert result['contract_card'] is None
        assert result['objects'] is None