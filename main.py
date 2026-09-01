from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from core.config import settings
from app.api.router import api_router


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Backend API for AI Engineering System"
)
@app.get("/")
def root():
    return {
        "message": "Welcome to AI Engineering System API",
        "docs_url": "/docs",
        "api_v1": settings.API_V1_STR
    }

# Include API endpoints
app.include_router(api_router, prefix="/api")
