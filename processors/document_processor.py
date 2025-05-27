"""Document processing for various file types."""

from typing import BinaryIO
import pandas as pd
from config.settings import Config

# Document processing imports
try:
    import PyPDF2
    from docx import Document
    import openpyxl
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

class DocumentProcessor:
    """Handle document processing for various file types."""
    
    @staticmethod
    def is_supported() -> bool:
        """Check if document processing is supported."""
        return PDF_SUPPORT
    
    @staticmethod
    def process_pdf(file: BinaryIO) -> str:
        """Extract text from PDF file."""
        try:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            return f"Error processing PDF: {str(e)}"
    
    @staticmethod
    def process_docx(file: BinaryIO) -> str:
        """Extract text from DOCX file."""
        try:
            doc = Document(file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            return f"Error processing DOCX: {str(e)}"
    
    @staticmethod
    def process_excel(file: BinaryIO) -> str:
        """Extract data from Excel file."""
        try:
            try:
                df = pd.read_excel(file, engine='openpyxl')
            except Exception:
                df = pd.read_excel(file, engine='xlrd')
            
            text = f"Excel Data Summary:\n"
            text += f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n\n"
            text += f"Columns: {', '.join(df.columns)}\n\n"
            text += "Data Preview:\n"
            text += df.head(10).to_string()
            
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                text += "\n\nNumeric Summary:\n"
                text += df[numeric_cols].describe().to_string()
            
            return text
        except Exception as e:
            return f"Error processing Excel: {str(e)}"
    
    @staticmethod
    def process_csv(file: BinaryIO) -> str:
        """Extract data from CSV file."""
        try:
            df = pd.read_csv(file)
            
            text = f"CSV Data Summary:\n"
            text += f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n\n"
            text += f"Columns: {', '.join(df.columns)}\n\n"
            text += "Data Preview:\n"
            text += df.head(10).to_string()
            
            numeric_cols = df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                text += "\n\nNumeric Summary:\n"
                text += df[numeric_cols].describe().to_string()
            
            return text
        except Exception as e:
            return f"Error processing CSV: {str(e)}"
    
    def process_file(self, uploaded_file, file_type: str) -> str:
        """Process file based on its type."""
        if not self.is_supported():
            return "Document processing not available. Please install required packages."
        
        if file_type == 'pdf':
            return self.process_pdf(uploaded_file)
        elif file_type == 'docx':
            return self.process_docx(uploaded_file)
        elif file_type in ['xlsx', 'xls']:
            return self.process_excel(uploaded_file)
        elif file_type == 'csv':
            return self.process_csv(uploaded_file)
        else:
            return f"Unsupported file type: {file_type}"