from app.core.database import SessionLocal, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship

class Documents(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), index=True)
    file_path = Column(String(255), index=True)
    created_at = Column(DateTime, index=True)
    updated_at = Column(DateTime, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("Users", back_populates="documents")

    __table_args__ = (
        Index("idx_documents_file_name", "file_name"),
        Index("idx_documents_file_path", "file_path"),
        Index("idx_documents_user_id", "user_id"),
        UniqueConstraint("user_id", "file_name", name="uq_user_file_name"),
    )

    @classmethod
    def create(cls, user_id: int, request:dict):
        db = SessionLocal()
        try:
            file_name = request.get("file_name")
            file_path = request.get("file_path")
            existing_document = db.query(cls).filter(cls.user_id == user_id, cls.file_name == file_name).first()
            if existing_document:
                raise Exception("Document with same name already exists for this user")
            new_document = cls(user_id=user_id, file_name=file_name, file_path=file_path)
            db.add(new_document)
            db.commit()
            db.refresh(new_document)
            return new_document
        except Exception as e:
            db.rollback()
            print(e)
            raise Exception(e)
        finally:
            db.close()
    
    @classmethod
    def get_documents_by_user_id(cls, user_id: int,file_name:str):
        db = SessionLocal()
        try:
            documents = db.query(cls).filter(cls.user_id == user_id, cls.file_name == file_name).first()
            return documents
        except Exception as e:
            db.rollback()
            print(e)
            raise Exception(e)
        finally:
            db.close()

    @classmethod
    def delete(cls, doc_id: int):
        db = SessionLocal()
        try:
            doc = db.query(cls).filter(cls.id == doc_id).first()
            if doc:
                db.delete(doc)
                db.commit()
                return True
            return False
        except Exception as e:
            db.rollback()
            print(e)
            return False
        finally:
            db.close()

    


    