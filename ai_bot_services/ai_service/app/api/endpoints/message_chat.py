from fastapi import APIRouter
from app.services import ai_core
from app.api.schemas.model_name import AIRequest

router = APIRouter(
    prefix="/ai_service",
    tags=["ai_service"],
)

# Прием запросов
@router.post("/chat")
async def chat_endpoint(request: AIRequest):
    return await ai_core.ai_message_request(request=request)

# Прием запросов
@router.post("/voice")
async def voice_endpoint(request: AIRequest):
    return await ai_core.voice_handler(request)

