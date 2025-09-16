from groq import Groq
from config import API_TOKEN
from logger import logger
from app.api.schemas.model_name import AIRequest

# Подключение к стороннему AI-API
client = Groq(
    api_key=API_TOKEN
)

# Отправка запроса
async def ai_request(request: AIRequest) -> str:

    try:
        logger.info(f"Выполняется запрос к модели {request.model.value}")

        # В начале задаем системный промт, для того, чтобы модель имела контекст.
        chat_completion = client.chat.completions.create(
            model=request.model.value,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — русскоязычный AI-ассистент. "
                        "Твоя задача помочь человеку с его запросом."
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