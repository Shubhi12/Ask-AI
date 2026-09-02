from app.core.config import settings
from app.ingestion.chunking.generate_chunks import ChunkerFactory
from app.ingestion.embeddings.embedding_service import EmbeddingService
from app.core.database import SessionLocal
from app.models.knowledge_base import KnowledgeBase

class IngesionPipeline:
    def __init__(self):
        self.embedding_service = EmbeddingService()
    
    def run(self, file_names: list[str], document_ids: list[int]):
        db = SessionLocal()
        try:
            chunker_obj = ChunkerFactory().get_chunking_strategy()
            for file_name, document_id in zip(file_names, document_ids):
                document_chunks = chunker_obj.generate_chunks(file_name)
                # batch process 10 chunks at a time
                for i in range(0, len(document_chunks), settings.TEXT_EMBED_BATCH_SIZE):
                    embed_chunks = []
                    batch = document_chunks[i:i+settings.TEXT_EMBED_BATCH_SIZE]
                    chunk_texts = [chunk["text"] for chunk in batch]
                    batch_embeddings = self.embedding_service.embed_texts(chunk_texts)
                    for j in range(len(batch)):
                        temp = {}
                        temp["embedding"] = batch_embeddings[j]
                        temp["meta"] = batch[j]
                        temp["content"] = batch[j]["text"]
                        temp["title"] = batch[j]["source"]
                        temp["document_id"] = document_id
                        embed_chunks.append(temp)
                    db.bulk_insert_mappings(KnowledgeBase, embed_chunks)
                    db.commit()
            db.flush()
        except Exception as e:
            db.rollback()
            print(e)
            raise Exception(e)
        finally:
            db.close()
