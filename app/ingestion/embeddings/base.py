from abc import ABC, abstractmethod


class EmbeddingsProvider(ABC):
    @abstractmethod
    def embed_text(self,text:str):
        pass
    
    @abstractmethod
    def embed_texts(self,texts:list[str]):
        pass
    