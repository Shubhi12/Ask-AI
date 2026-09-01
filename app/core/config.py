import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Engineering"
    API_V1_STR: str = "/api"
    MAX_CONVERSATION_LENGTH: int = 10
    MAX_CONVERSATION_THREAD_COUNT: int = 5
    PROJECT_ROOT_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    DOCUMENT_PATH: str = os.path.join(PROJECT_ROOT_DIR, "documents")
    EMBEDDING_MODEL: str = "liquid/lfm-2.5-embedding-350m:free"
    TEXT_EMBED_BATCH_SIZE: int = 10
    

    # SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkeyforcreatorteamplatform")
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080 # 7 days
    
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "learn_ai_engineering")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "6543")

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    S3_ENDPOINT_URL: str = os.getenv("S3_ENDPOINT_URL", "")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "upload_company_docs")
    S3_STORAGE_REGION: str = os.getenv("S3_STORAGE_REGION", "ap-northeast-1")
    S3_SECRET_ACCESS_KEY: str = os.getenv("S3_SECRET_ACCESS_KEY", "")
    S3_ACCESS_KEY: str = os.getenv("S3_ACCESS_KEY", "")

    REDIS_URL: str = os.getenv("REDIS_URL") or "redis://redis:6379/0"
    
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL") or "redis://redis:6379/0"
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND") or "redis://redis:6379/0"



    

    class Config:
        case_sensitive = True

settings = Settings()
