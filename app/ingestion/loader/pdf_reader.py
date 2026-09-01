from app.core.config import settings
from pypdf import PdfReader
from app.ingestion.loader.base import LoadDocument

class PDFReader(LoadDocument):
    def __init__(self, file_name:str):
        self.file_path = settings.DOCUMENT_PATH+"/"+file_name

    def load_document(self):
        try:
            return PdfReader(self.file_path)
        except Exception as e:
            print(f"ERROR in load_document: {e}")
            raise Exception(e)
