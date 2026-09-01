from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship
from datetime import datetime
from core.database import SessionLocal, Base

class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    meta = Column("metadata", JSONB)
    embedding = Column(Vector(1024))
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    @staticmethod
    def search_vector_similarity(query_embedding: list, k: int = 3) -> list:
        """Search query vector in knowledge base and return top k similar vectors."""
        db = SessionLocal() 
        try:
            results = (
                db.query(
                    KnowledgeBase,
                    KnowledgeBase.embedding.cosine_distance(query_embedding).label("distance")
                )
                .order_by("distance")
                .limit(k)
                .all()
            )

            return [
                {
                    "id": row.KnowledgeBase.id,
                    "content": row.KnowledgeBase.content,
                    "similarity_score": 1.0 - float(row.distance) if row.distance is not None else 0.0
                }
                for row in results
            ]
        except Exception as e:
            print(f"ERROR in search_vector_similarity: {e}")
            raise Exception(e)
        finally:
            db.close()