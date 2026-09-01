from core.config import settings
from app.services.rag.chunking_techniques.generate_chunks import GenerateChunksFactory
from app.services.llm_services import LLMServices
from core.database import SessionLocal
from models.knowledge_base import KnowledgeBase

class IngesionPipeline:
    def __init__(self):
        self.llm_services = LLMServices()
    
    def run(self, file_name: str):
        db = SessionLocal()
        try:
            generate_chunks_obj = GenerateChunksFactory()
            document_chunks = generate_chunks_obj.generate_chunks(file_name)
            # batch process 10 chunks at a time
            for i in range(0, len(document_chunks), settings.TEXT_EMBED_BATCH_SIZE):
                embed_chunks = []
                batch = document_chunks[i:i+settings.TEXT_EMBED_BATCH_SIZE]
                chunk_texts = [chunk["text"] for chunk in batch]
                batch_embeddings = self.llm_services.embed_text(chunk_texts, settings.EMBEDDING_MODEL)
                for j in range(len(batch)):
                    temp = {}
                    temp["embedding"] = batch_embeddings[j]
                    temp["meta"] = batch[j]
                    temp["content"] = batch[j]["text"]
                    temp["title"] = file_name.split(".")[0]
                    embed_chunks.append(temp)
                print(embed_chunks)                
                db.bulk_insert_mappings(KnowledgeBase, embed_chunks)
                db.commit()
        except Exception as e:
            db.rollback()
            print(e)
            raise Exception(e)
        finally:
            db.close()
