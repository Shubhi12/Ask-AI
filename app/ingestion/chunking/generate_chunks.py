from app.ingestion.loader.pdf_reader import PDFReader
from app.ingestion.chunking.recursive_chunks import RecursiveChunks
from app.ingestion.chunking.fixsize_chunks import FixSizeChunkes


class ChunkerFactory():
    @staticmethod
    def get_chunking_strategy(strategy:str=None):
        if strategy == "fixed_size":
            return FixSizeChunkes()
        else:
            return RecursiveChunks()