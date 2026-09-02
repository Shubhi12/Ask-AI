from app.core import database
from app.core.config import settings
import math
from app.services.llm_services import LLMServices
from app.ingestion.embeddings.base import EmbeddingsProvider

class EmbeddingService(EmbeddingsProvider):
    def __init__(self):
        self.llm_services = LLMServices()
    
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.llm_services.embed_text(texts)
        if not isinstance(embeddings, list):
            raise ValueError(f"Expected list of embeddings, but received {type(embeddings)}: {embeddings}")
        if embeddings and not isinstance(embeddings[0], (list, tuple)):
            raise ValueError(f"Expected list of numerical vectors, but received element of type {type(embeddings[0])}")
        return embeddings
    
    def embed_text(self, text: str) -> list[float]:
        embeddings = self.embed_texts([text])
        if not embeddings:
            raise ValueError("Failed to obtain embedding for text")
        return embeddings[0]



    def cosine_similarity(self,a:list,b:list)->float:
        """Calculate the cosine similarity between two vectors.
            """
        dot_product = sum(x * y for x, y in zip(a, b))
        magnitude_a = math.sqrt(sum(x * x for x in a))
        magnitude_b = math.sqrt(sum(x * x for x in b))

        return dot_product / (magnitude_a * magnitude_b)
        
