from fastapi import APIRouter
from app.config import settings

router = APIRouter()

@router.get("/health")
def health():
    return {
        "status": "ok",
        "ai_configured": bool(
            settings.llm_base_url and settings.llm_api_key and settings.llm_model
        ),
    }
