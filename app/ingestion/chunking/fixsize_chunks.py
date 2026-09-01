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

        