"""
Tests for document text extraction service.
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from app.services.docs.extractor import DocumentExtractor, extract_text


class TestDocumentExtractor:
    """Test cases for DocumentExtractor class."""
    
    @pytest.fixture
    def extractor(self):
        """Create a DocumentExtractor instance for testing."""
        return DocumentExtractor(ocr_fallback=False)
    
    @pytest.fixture
    def extractor_with_ocr(self):
        """Create a DocumentExtractor instance with OCR fallback enabled."""
        return DocumentExtractor(ocr_fallback=True)
    
    @pytest.fixture
    def test_files_dir(self):
        """Get the path to test fixtures directory."""
        return Path(__file__).parent / "fixtures"
    
    @pytest.fixture
    def pdf_file(self, test_files_dir):
        """Get path to test PDF file."""
        return test_files_dir / "test_document.pdf"
    
    @pytest.fixture
    def docx_file(self, test_files_dir):
        """Get path to test DOCX file."""
        return test_files_dir / "test_document.docx"
    
    @pytest.fixture
    def html_file(self, test_files_dir):
        """Get path to test HTML file."""
        return test_files_dir / "test_document.html"
    
    @pytest.fixture
    def txt_file(self, test_files_dir):
        """Get path to test text file."""
        return test_files_dir / "test_document.txt"
    
    def test_extractor_initialization(self):
        """Test DocumentExtractor initialization."""
        # Test with OCR fallback enabled
        extractor_with_ocr = DocumentExtractor(ocr_fallback=True)
        assert extractor_with_ocr.ocr_fallback is True
        
        # Test with OCR fallback disabled
        extractor_without_ocr = DocumentExtractor(ocr_fallback=False)
        assert extractor_without_ocr.ocr_fallback is False
    
    def test_extract_from_pdf(self, extractor, pdf_file):
        """Test text extraction from PDF file."""
        # Ensure test file exists
        assert pdf_file.exists(), f"Test PDF file not found: {pdf_file}"
        
        # Extract text
        text = extractor.extract_text(pdf_file)
        
        # Verify text was extracted
        assert isinstance(text, str)
        assert len(text) > 0
        
        # Verify specific keywords are present
        assert "EXTRACTION_TEST" in text
        assert "PDF_DOCUMENT" in text
        assert "SAMPLE_CONTENT" in text
        
        # Verify other expected content
        assert "Test PDF Document" in text
        assert "quick brown fox" in text.lower()
        
        print(f"PDF extraction successful. Text length: {len(text)} characters")
        print(f"First 200 chars: {text[:200]}...")
    
    def test_extract_from_docx(self, extractor, docx_file):
        """Test text extraction from DOCX file."""
        # Ensure test file exists
        assert docx_file.exists(), f"Test DOCX file not found: {docx_file}"
        
        # Extract text
        text = extractor.extract_text(docx_file)
        
        # Verify text was extracted
        assert isinstance(text, str)
        assert len(text) > 0
        
        # Verify specific keywords are present
        assert "EXTRACTION_TEST" in text
        assert "DOCX_DOCUMENT" in text
        assert "SAMPLE_CONTENT" in text
        
        # Verify other expected content
        assert "Test DOCX Document" in text
        assert "quick brown fox" in text.lower()
        
        # Verify table content was extracted
        assert "Column 1" in text or "Column 2" in text or "Column 3" in text
        
        print(f"DOCX extraction successful. Text length: {len(text)} characters")
        print(f"First 200 chars: {text[:200]}...")
    
    def test_extract_from_html(self, extractor, html_file):
        """Test text extraction from HTML file."""
        # Ensure test file exists
        assert html_file.exists(), f"Test HTML file not found: {html_file}"
        
        # Extract text
        text = extractor.extract_text(html_file)
        
        # Verify text was extracted
        assert isinstance(text, str)
        assert len(text) > 0
        
        # Verify specific keywords are present
        assert "EXTRACTION_TEST" in text
        assert "HTML_DOCUMENT" in text
        assert "SAMPLE_CONTENT" in text
        
        # Verify other expected content
        assert "Test HTML Document" in text
        assert "quick brown fox" in text.lower()
        
        # Verify HTML tags were removed
        assert "<" not in text or ">" not in text
        
        print(f"HTML extraction successful. Text length: {len(text)} characters")
        print(f"First 200 chars: {text[:200]}...")
    
    def test_extract_from_text(self, extractor, txt_file):
        """Test text extraction from plain text file."""
        # Ensure test file exists
        assert txt_file.exists(), f"Test text file not found: {txt_file}"
        
        # Extract text
        text = extractor.extract_text(txt_file)
        
        # Verify text was extracted
        assert isinstance(text, str)
        assert len(text) > 0
        
        # Verify specific keywords are present
        assert "EXTRACTION_TEST" in text
        assert "PDF_DOCUMENT" in text  # Note: This is in the text file content
        assert "SAMPLE_CONTENT" in text
        
        # Verify other expected content
        assert "Test Document for Extraction Service" in text
        assert "quick brown fox" in text.lower()
        
        print(f"Text file extraction successful. Text length: {len(text)} characters")
    
    def test_extract_text_cleanup(self, extractor, txt_file):
        """Test that extracted text is properly cleaned."""
        # Extract text
        text = extractor.extract_text(txt_file)
        
        # Verify text is cleaned (no excessive whitespace)
        lines = text.split('\n')
        for line in lines:
            # Each line should not have leading/trailing whitespace
            assert line == line.strip()
            # No line should be empty (unless it's meaningful empty line)
            # But in cleaned text, empty lines between paragraphs are preserved as single newlines
        
        # Verify no weird characters (basic ASCII check)
        # Allow common punctuation and letters
        import string
        allowed_chars = string.printable + "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
        for char in text:
            if char not in allowed_chars and ord(char) > 127:
                # Allow Unicode characters but log them
                print(f"Non-ASCII character found: {char} (ord: {ord(char)})")
    
    def test_file_not_found(self, extractor):
        """Test extraction from non-existent file."""
        non_existent_file = Path("/tmp/non_existent_file_12345.pdf")
        
        with pytest.raises(FileNotFoundError):
            extractor.extract_text(non_existent_file)
    
    def test_unsupported_format(self, extractor, tmp_path):
        """Test extraction from unsupported file format."""
        # Create a file with unsupported extension
        unsupported_file = tmp_path / "test.unsupported"
        unsupported_file.write_text("Test content")
        
        with pytest.raises(ValueError) as exc_info:
            extractor.extract_text(unsupported_file)
        
        assert "Unsupported file format" in str(exc_info.value)
    
    def test_extract_text_from_bytes(self, extractor, pdf_file):
        """Test extraction from file bytes."""
        # Read file as bytes
        with open(pdf_file, 'rb') as f:
            file_bytes = f.read()
        
        # Extract text from bytes
        text = extractor.extract_text_from_bytes(file_bytes, '.pdf')
        
        # Verify text was extracted
        assert isinstance(text, str)
        assert len(text) > 0
        
        # Verify specific keywords are present
        assert "EXTRACTION_TEST" in text
        assert "PDF_DOCUMENT" in text
    
    def test_convenience_function(self, pdf_file):
        """Test the convenience extract_text function."""
        text = extract_text(pdf_file, ocr_fallback=False)
        
        # Verify text was extracted
        assert isinstance(text, str)
        assert len(text) > 0
        
        # Verify specific keywords are present
        assert "EXTRACTION_TEST" in text
        assert "PDF_DOCUMENT" in text
    
    @patch('app.services.docs.extractor.OCR_AVAILABLE', False)
    def test_ocr_fallback_not_available(self, extractor, tmp_path):
        """Test behavior when OCR fallback is requested but not available."""
        # Create a file that will fail extraction
        test_file = tmp_path / "test.bin"
        test_file.write_bytes(b"Binary content that can't be extracted as text")
        
        # This should fail since it's not a supported format
        with pytest.raises(ValueError):
            extractor.extract_text(test_file)
    
    @patch('app.services.docs.extractor.OCR_AVAILABLE', True)
    @patch('app.services.docs.extractor.pytesseract')
    @patch('app.services.docs.extractor.Image')
    def test_ocr_fallback_mock(self, mock_image, mock_pytesseract, extractor_with_ocr, tmp_path):
        """Test OCR fallback with mocked dependencies."""
        # Use the extractor_with_ocr fixture
        extractor = extractor_with_ocr
        
        # Create a file that will fail regular extraction
        test_file = tmp_path / "test.fake_pdf"
        test_file.write_text("This looks like a PDF but isn't")
        
        # Mock the OCR dependencies
        mock_image_instance = MagicMock()
        mock_image.open.return_value = mock_image_instance
        mock_pytesseract.image_to_string.return_value = "OCR extracted text"
        
        # Mock the extraction to fail
        with patch.object(extractor, '_extract_from_pdf', side_effect=Exception("Extraction failed")):
            # This should trigger OCR fallback
            text = extractor.extract_text(test_file)
            
            # Verify OCR was called
            assert text == "OCR extracted text"
            mock_pytesseract.image_to_string.assert_called_once_with(mock_image_instance)
    
    def test_error_handling(self, extractor, tmp_path):
        """Test error handling during extraction."""
        # Create a corrupted PDF file
        corrupted_pdf = tmp_path / "corrupted.pdf"
        corrupted_pdf.write_bytes(b"Not a valid PDF file")
        
        # This should raise an exception
        with pytest.raises(Exception):
            extractor.extract_text(corrupted_pdf)
    
    def test_clean_text_method(self, extractor):
        """Test the _clean_text method directly."""
        # Test with messy text
        messy_text = "  Hello   World  \n\n  This  is  a  test  \n  \n  "
        cleaned = extractor._clean_text(messy_text)
        
        expected = "Hello World\nThis is a test"
        assert cleaned == expected
        
        # Test with empty text
        assert extractor._clean_text("") == ""
        
        # Test with only whitespace
        assert extractor._clean_text("   \n  \n  ") == ""
        
        # Test with Unicode text
        unicode_text = "Привет мир\nHello world"
        cleaned_unicode = extractor._clean_text(unicode_text)
        assert "Привет мир" in cleaned_unicode
        assert "Hello world" in cleaned_unicode


if __name__ == "__main__":
    # Run tests directly for debugging
    import sys
    pytest.main([__file__, "-v"])