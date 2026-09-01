from abc import ABC, abstractmethod

class LoadDocument(ABC):
    @abstractmethod
    def load_document(self):
        pass
    