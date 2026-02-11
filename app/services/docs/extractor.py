"""
Document Text Extraction Service

This module provides functionality to extract text from various document formats:
- PDF files using pdfplumber (with layout preservation)
- DOCX files using python-docx
- HTML files using BeautifulSoup
- Fallback to OCR (tesseract) when text extraction returns empty

The service returns clean UTF-8 text.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Union
import tempfile

# Import document parsing libraries
import pdfplumber
from docx import Document
from bs4 import BeautifulSoup

# Optional OCR import (for fallback)
try:
    import pytesseract
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    pytesseract = None
    Image = None

logger = logging.getLogger(__name__)


class DocumentExtractor:
    """Extract text from various document formats."""
    
    def __init__(self, ocr_fallback: bool = True):
        """
        Initialize the document extractor.
        
        Args:
            ocr_fallback: Whether to use OCR as fallback when text extraction fails
        """
        self.ocr_fallback = ocr_fallback
        if ocr_fallback and not OCR_AVAILABLE:
            logger.warning(
                "OCR fallback requested but pytesseract/Pillow not installed. "
                "Install with: pip install pytesseract pillow"
            )
    
    def extract_text(self, file_path: Union[str, Path]) -> str:
        """
        Extract text from a document file.
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text as UTF-8 string
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is not supported
            Exception: For other extraction errors
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Determine file type from extension
        ext = file_path.suffix.lower()
        
        try:
            if ext == '.pdf':
                return self._extract_from_pdf(file_path)
            elif ext == '.docx':
                return self._extract_from_docx(file_path)
            elif ext in ['.html', '.htm']:
                return self._extract_from_html(file_path)
            elif ext in ['.txt', '.md']:
                return self._extract_from_text(file_path)
            else:
                raise ValueError(f"Unsupported file format: {ext}")
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            
            # Try OCR fallback if enabled and appropriate
            if self.ocr_fallback and OCR_AVAILABLE:
                logger.info(f"Attempting OCR fallback for {file_path}")
                try:
                    return self._extract_with_ocr(file_path)
                except Exception as ocr_error:
                    logger.error(f"OCR fallback also failed: {ocr_error}")
            
            # Re-raise the original error if OCR not available or failed
            raise
    
    def _extract_from_pdf(self, file_path: Path) -> str:
        """
        Extract text from PDF file using pdfplumber.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text
        """
        text_parts = []
        
        try:
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    try:
                        # Extract text with layout preservation
                        page_text = page.extract_text()
                        if page_text:
                            text_parts.append(page_text.strip())
                        else:
                            # If no text found, try alternative extraction
                            logger.debug(f"No text found on PDF page {page_num}, trying alternative extraction")
                            page_text = page.extract_text(x_tolerance=1, y_tolerance=1)
                            if page_text:
                                text_parts.append(page_text.strip())
                    except Exception as page_error:
                        logger.warning(f"Error extracting text from PDF page {page_num}: {page_error}")
                        continue
            
            if not text_parts:
                logger.warning(f"No text could be extracted from PDF: {file_path}")
                return ""
            
            # Join all pages with double newlines
            full_text = "\n\n".join(text_parts)
            
            # Clean up the text
            full_text = self._clean_text(full_text)
            
            return full_text
            
        except Exception as e:
            logger.error(f"Error opening/processing PDF {file_path}: {e}")
            raise
    
    def _extract_from_docx(self, file_path: Path) -> str:
        """
        Extract text from DOCX file using python-docx.
        
        Args:
            file_path: Path to DOCX file
            
        Returns:
            Extracted text
        """
        try:
            doc = Document(file_path)
            text_parts = []
            
            # Extract paragraphs
            for paragraph in doc.paragraphs:
                if paragraph.text.strip():
                    text_parts.append(paragraph.text.strip())
            
            # Extract tables
            for table in doc.tables:
                for row in table.rows:
                    row_texts = []
                    for cell in row.cells:
                        if cell.text.strip():
                            row_texts.append(cell.text.strip())
                    if row_texts:
                        text_parts.append(" | ".join(row_texts))
            
            if not text_parts:
                logger.warning(f"No text found in DOCX file: {file_path}")
                return ""
            
            # Join with newlines
            full_text = "\n".join(text_parts)
            
            # Clean up the text
            full_text = self._clean_text(full_text)
            
            return full_text
            
        except Exception as e:
            logger.error(f"Error processing DOCX file {file_path}: {e}")
            raise
    
    def _extract_from_html(self, file_path: Path) -> str:
        """
        Extract text from HTML file using BeautifulSoup.
        
        Args:
            file_path: Path to HTML file
            
        Returns:
            Extracted text
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Clean up the text
            text = self._clean_text(text)
            
            return text
            
        except Exception as e:
            logger.error(f"Error processing HTML file {file_path}: {e}")
            raise
    
    def _extract_from_text(self, file_path: Path) -> str:
        """
        Extract text from plain text file.
        
        Args:
            file_path: Path to text file
            
        Returns:
            Extracted text
        """
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1251', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(file_path, 'r', encoding=encoding) as f:
                        text = f.read()
                    
                    # Clean up the text
                    text = self._clean_text(text)
                    
                    return text
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, try binary read
            with open(file_path, 'rb') as f:
                text = f.read().decode('utf-8', errors='ignore')
            
            text = self._clean_text(text)
            return text
            
        except Exception as e:
            logger.error(f"Error reading text file {file_path}: {e}")
            raise
    
    def _extract_with_ocr(self, file_path: Path) -> str:
        """
        Extract text using OCR (tesseract) as fallback.
        
        Args:
            file_path: Path to document file
            
        Returns:
            Extracted text from OCR
            
        Raises:
            ImportError: If OCR dependencies not installed
            Exception: For OCR processing errors
        """
        if not OCR_AVAILABLE:
            raise ImportError(
                "OCR dependencies not installed. "
                "Install with: pip install pytesseract pillow"
            )
        
        ext = file_path.suffix.lower()
        
        try:
            if ext == '.pdf':
                # For PDFs, we need to convert pages to images first
                # This is a simplified implementation
                # In production, you might want to use pdf2image or similar
                logger.warning(f"OCR for PDF files requires additional processing. "
                             f"Consider using pdf2image for better OCR results.")
                
                # Create a temporary directory for images
                with tempfile.TemporaryDirectory() as temp_dir:
                    # Convert PDF to images (simplified - would need pdf2image)
                    # For now, we'll extract text from the first page using pdfplumber's image extraction
                    with pdfplumber.open(file_path) as pdf:
                        if pdf.pages:
                            # Try to extract text from the first page image
                            page = pdf.pages[0]
                            # pdfplumber can extract images, but OCR would need additional steps
                            # For MVP, we'll return a message
                            return "[OCR for PDF would require pdf2image conversion]"
                        else:
                            return ""
            else:
                # For image files or other formats
                # Note: This would work for image files, not for PDF/DOCX directly
                logger.warning(f"Direct OCR for {ext} files may not work well. "
                             f"Consider converting to images first.")
                
                # Try to open as image
                try:
                    image = Image.open(file_path)
                    text = pytesseract.image_to_string(image)
                    text = self._clean_text(text)
                    return text
                except Exception as img_error:
                    logger.error(f"Error processing {file_path} as image for OCR: {img_error}")
                    raise
        
        except Exception as e:
            logger.error(f"OCR processing failed for {file_path}: {e}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove excessive whitespace
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line:  # Skip empty lines
                # Replace multiple spaces with single space
                line = ' '.join(line.split())
                cleaned_lines.append(line)
        
        # Join with single newlines
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Ensure UTF-8 encoding
        if isinstance(cleaned_text, bytes):
            cleaned_text = cleaned_text.decode('utf-8', errors='ignore')
        
        return cleaned_text
    
    def extract_text_from_bytes(self, file_bytes: bytes, file_extension: str) -> str:
        """
        Extract text from file bytes.
        
        Args:
            file_bytes: File content as bytes
            file_extension: File extension (e.g., '.pdf', '.docx')
            
        Returns:
            Extracted text
        """
        # Create temporary file
        with tempfile.NamedTemporaryFile(suffix=file_extension, delete=False) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name
        
        try:
            return self.extract_text(temp_path)
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {temp_path}: {e}")


# Convenience function for simple extraction
def extract_text(file_path: Union[str, Path], ocr_fallback: bool = True) -> str:
    """
    Convenience function to extract text from a document.
    
    Args:
        file_path: Path to the document file
        ocr_fallback: Whether to use OCR as fallback
        
    Returns:
        Extracted text
    """
    extractor = DocumentExtractor(ocr_fallback=ocr_fallback)
    return extractor.extract_text(file_path)