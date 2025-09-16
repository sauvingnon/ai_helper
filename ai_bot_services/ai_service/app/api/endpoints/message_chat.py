from fastapi import APIRouter
from app.services import ai_core
from app.api.schemas.model_name import AIRequest

router = APIRouter(
    prefix="/ai_service",
    tags=["ai_service"],
)

# Прием запросов
@router.post("/chat")
async def add_client(request: AIRequest):
    return await ai_core.ai_request(request=request)
