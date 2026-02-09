"""
PDF Parser Module
Handles extraction of text from PDF and TXT documents
"""
import os
from pathlib import Path
from typing import Optional

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False


class DocumentParser:
    """Parse FNOL documents from various formats"""
    
    SUPPORTED_FORMATS = [".pdf", ".txt"]
    
    def __init__(self):
        self.supported_formats = self.SUPPORTED_FORMATS
    
    def parse_document(self, file_path: str) -> Optional[str]:
        """
        Parse a document and extract text
        
        Args:
            file_path: Path to the document file
            
        Returns:
            Extracted text from the document, or None if parsing fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Document not found: {file_path}")
        
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == ".txt":
            return self._parse_txt(file_path)
        elif file_ext == ".pdf":
            return self._parse_pdf(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    def _parse_txt(self, file_path: str) -> str:
        """Parse text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise Exception(f"Error reading TXT file: {str(e)}")
    
    def _parse_pdf(self, file_path: str) -> str:
        """Parse PDF file"""
        if not HAS_PDFPLUMBER:
            raise ImportError("pdfplumber is required for PDF parsing. Install with: pip install pdfplumber")
        
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
                    text += "\n"
            return text
        except Exception as e:
            raise Exception(f"Error reading PDF file: {str(e)}")
    
    def is_supported_format(self, file_path: str) -> bool:
        """Check if file format is supported"""
        file_ext = Path(file_path).suffix.lower()
        return file_ext in self.SUPPORTED_FORMATS
