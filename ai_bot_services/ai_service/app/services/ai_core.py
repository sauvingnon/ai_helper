from groq import Groq
from config import API_TOKEN
from logger import logger
from app.api.schemas.model_name import AIRequest

client = Groq(
    api_key=API_TOKEN
)

async def ai_request(request: AIRequest) -> str:

    try:

        logger.info(f"Выполняется запрос к модели {request.model.value}")

        chat_completion = client.chat.completions.create(
            model=request.model.value,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — русскоязычный AI-ассистент. "
                        "Отвечай строго на русском языке, даже если вопрос на английском."
                    ),
                },
                {
                    "role": "user",
                    "content": request.message  # это уже реальный вопрос пользователя
                }
            ],
        )

        result = chat_completion.choices[0].message.content

        logger.info(f"Запрос выполнен успешно")

        return result
    
    except Exception as e:
       logger.exception(f"Ошибка при выполнении запроса: {e}")
       return None