from core.config import settings
from pypdf import PdfReader
from app.services.rag.interfaces.document_loader import LoadDocument

class PDFReader(LoadDocument):
    def __init__(self, file_name:str):
        self.file_path = settings.DOCUMENT_PATH+"/"+file_name

    def load_document(self):
        return PdfReader(self.file_path)
