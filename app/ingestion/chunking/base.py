from abc import ABC, abstractmethod


class ChunkingStrategy(ABC):
    @abstractmethod
    def chunking(self,text:str):
        pass

    @abstractmethod
    def generate_chunks(self,file_name:str):
        pass