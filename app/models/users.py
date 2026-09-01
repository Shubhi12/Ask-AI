from datetime import datetime
from app.core.database import SessionLocal,Base
from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.orm import relationship

class Users(Base):
   __tablename__ = "users"
   id = Column(Integer, primary_key=True, index=True)
   username = Column(String(255), index=True)
   email = Column(String(255), index=True)
   password = Column(String(255), index=True)
   company_name = Column(String(255), index=True)
   description = Column(String(255), index=True)
   created_at = Column(DateTime, index=True)
   updated_at = Column(DateTime, index=True)
      # Matches the property name 'user' in Documents
   documents = relationship("Documents", back_populates="user")

   # create index for email and username
   __table_args__ = (
      Index("idx_user_email", "email"),
      Index("idx_user_username", "username"),
   )

    # def is_authenticated(self):
    #     return True
   
   @classmethod
   def create(cls,user_data:dict):
       db = SessionLocal()
       try:
           user = cls(**user_data)
           db.add(user)
           db.commit()
           db.refresh(user)
           return user
       except Exception as e:
           db.rollback()
           print(e)
           raise Exception(e)
       finally:
           db.close()
   
   @classmethod
   def update(cls,user_data:dict):
       db = SessionLocal()
       try:
           user = db.query(Users).filter(Users.id == cls.id).first()
           user.username = user_data.get("username", user.username)
           user.email = user_data.get("email", user.email)
           user.password = user_data.get("password", user.password)
           user.company_name = user_data.get("company_name", user.company_name)
           user.description = user_data.get("description", user.description)
           user.updated_at = datetime.utcnow()
           db.commit()
           db.refresh(user)
           return user
       except Exception as e:
           db.rollback()
           print(e)
           raise Exception(e)
       finally:
           db.close()

   @classmethod
   def get_user_by_email(cls,email:str):
       db = SessionLocal()
       try:
           user = db.query(Users).filter(Users.email == email).first()
           return user
       except Exception as e:
           db.rollback()
           print(e)
           raise Exception(e)
       finally:
           db.close()
    
   @classmethod
   def get_user_by_username(cls,username:str):
        db = SessionLocal()
        try:
            user = db.query(Users).filter(Users.username == username).first()
            return user
        except Exception as e:
            db.rollback()
            print(e)
            raise Exception(e)
        finally:
            db.close()