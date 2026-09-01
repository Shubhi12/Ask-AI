from app.services.rag.interfaces.chunking_strategy import ChunkingStrategy

class RecursiveChunks(ChunkingStrategy):
    def __init__(self):
        super().__init__()
        self.delimiters = ["\n\n", "\n", ".", ","]
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
        
            

        
