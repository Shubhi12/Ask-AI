from app.services.helpers import get_file_name
from app.ingestion.loader.pdf_reader import PDFReader
from app.ingestion.chunking.base import ChunkingStrategy

class RecursiveChunks(ChunkingStrategy):
    def __init__(self):
        super().__init__()
        self.delimiters = ["\n\n", "\n", "."]
        self.chunks = []

    def chunking(self, text: str, delimiter_index: int = 0):
        if delimiter_index == 0:
            self.chunks = []

        if delimiter_index >= len(self.delimiters):
            if text:
                self.chunks.append(text)
            return self.chunks

        delimiter = self.delimiters[delimiter_index]
        if delimiter in text:
            seperate_text = text.split(delimiter)
            for chunk in seperate_text:
                self.chunking(chunk, delimiter_index + 1)
        else:
            self.chunking(text, delimiter_index + 1)

        return self.chunks

    def generate_chunks(self, file_path:str):
        document = PDFReader(file_path).load_document()
        chunks=[]
        for page_number, page in enumerate(document.pages, start=1):
            for chunk in self.chunking(page.extract_text()):
                chunk_metadata = {
                    "source": get_file_name(file_path),
                    "page": page_number,
                    "text": chunk
                }   
                chunks.append(chunk_metadata)
        return chunks
            

        
