from app.services.helpers import get_file_name
from app.ingestion.loader.pdf_reader import PDFReader
from app.ingestion.chunking.base import ChunkingStrategy

CHUNK_SIZE=500
CHUNK_OVERLAP=50

class FixSizeChunkes(ChunkingStrategy):
    def __init__(self, chunk_size=CHUNK_SIZE,chunk_overlap=CHUNK_OVERLAP):
        super().__init__()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunking(self,text:str):
        chunks=[]
        for i in range(0,len(text),self.chunk_size):
            chunks.append(text[i:i+self.chunk_size+self.chunk_overlap])
        return chunks

    def generate_chunks(self, file_name:str):
        document = PDFReader(file_name).load_document()
        chunks=[]
        for page_number, page in enumerate(document.pages, start=1):
            for chunk in self.chunking(page.extract_text()):
                chunk_metadata = {
                    "source": get_file_name(file_name),
                    "page": page_number,
                    "text": chunk
                }   
                chunks.append(chunk_metadata)
        return chunks


        