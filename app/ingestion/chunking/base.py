from abc import ABC, abstractmethod


class ChunkingStrategy(ABC):
    @abstractmethod
    def chunking(self,text:str):
        pass
        