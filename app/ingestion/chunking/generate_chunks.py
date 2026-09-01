from app.ingestion.loader.pdf_reader import PDFReader
from app.ingestion.chunking.recursive_chunks import RecursiveChunks


class GenerateChunksFactory():
    @staticmethod
    def get_chunking_strategy(strategy:str):
        if strategy == "recursive":
            return RecursiveChunks()
        else:
            raise ValueError("Invalid chunking strategy")
    

    def generate_chunks(self, file_name:str):
        document = PDFReader(file_name).load_document()
        chunks=[]
        for page_number, page in enumerate(document.pages, start=1):
            chunking_strategy = self.get_chunking_strategy("recursive")
            for chunk in chunking_strategy.chunking(page.extract_text()):
                chunk_metadata = {
                    "source": file_name,
                    "page": page_number,
                    "text": chunk
                }   
                chunks.append(chunk_metadata)
        return chunks