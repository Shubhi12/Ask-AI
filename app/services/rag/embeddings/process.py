from core import database
from core.config import settings
import math
from app.services.llm_services import LLMServices

class EmbeddingsProcess:
    def __init__(self):
        self.llm_services = LLMServices()
    
    def embed_text(self,text:str)->list:
        embedding = self.llm_services.embed_text([text], settings.EMBEDDING_MODEL)
        return embedding[0]



    def cosine_similarity(self,a:list,b:list)->float:
        """Calculate the cosine similarity between two vectors.
            """
        dot_product = sum(x * y for x, y in zip(a, b))
        magnitude_a = math.sqrt(sum(x * x for x in a))
        magnitude_b = math.sqrt(sum(x * x for x in b))

        return dot_product / (magnitude_a * magnitude_b)
        
