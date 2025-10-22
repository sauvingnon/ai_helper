# services/ai_service/ai_service.py

from app.services.ai_service.client import client
from typing import Optional
from app.schemas.ai_service import AIRequest, AIAudioResponse
from app.schemas.pyndantic import to_pydantic_model

entity_schema = "ai_service"

async def get_answer_for_text(request: AIRequest) -> Optional[str]:
    """
    Получить ответ на вопрос.
    """
    response = await client.post(
        f"{entity_schema}/chat",
        json=request.dict()   # <-- добавляем query-параметр
    )
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()

async def get_answer_for_audio(request: AIRequest) -> Optional[AIAudioResponse]:
    """
    Получить ответ на вопрос.
    """
    response = await client.post(
        f"{entity_schema}/voice",
        json=request.dict()   # <-- добавляем query-параметр
    )
    if response.status_code == 404:
        return None
    response_data = response.json()
    return to_pydantic_model(AIAudioResponse, response_data)