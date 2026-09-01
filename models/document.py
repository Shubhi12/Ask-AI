from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import relationship
from core.database import Base

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


    