from fastapi import APIRouter
from app.core.router import process_message
from app.api.schemas.model_name import AIRequest

router = APIRouter(
    prefix="/ai_service",
    tags=["ai_service"],
)

# Прием запросов
@router.post("/chat")
async def chat_endpoint(request: AIRequest):
    return await process_message(request=request)

# Прием запросов
@router.post("/voice")
async def voice_endpoint(request: AIRequest):
    return await process_message(request)

