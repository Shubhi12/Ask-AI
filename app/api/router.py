from fastapi import APIRouter
from app.api.endpoints import chat, classify, extract, generate, summarize, ask
from app.api.admin import auth as admin_auth, upload as admin_upload
api_router = APIRouter()

@api_router.get("/health", tags=["health"])
def health_check():
    return {
        "message": "AI Engineering System is running",
    }

api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(classify.router, prefix="/classify", tags=["classify"])
api_router.include_router(extract.router, prefix="/extract", tags=["extract"])
api_router.include_router(generate.router, prefix="/generate", tags=["generate"])
api_router.include_router(summarize.router, prefix="/summarize", tags=["summarize"])
api_router.include_router(ask.router, prefix="", tags=["ask"])
api_router.include_router(admin_auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(admin_upload.router, prefix="/upload", tags=["upload"])
