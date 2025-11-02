from openai import OpenAI
from config import API_TOKEN_DEEPSEEK, BASE_URL_DEEPSEEK
from logger import logger
from app.api.schemas.model_name import AIRequest

# Инициализация клиента
client = OpenAI(api_key=API_TOKEN_DEEPSEEK, base_url=BASE_URL_DEEPSEEK)

# --- 💬 Chat LLM ---
async def ai_message_request(request: AIRequest) -> str | None:
    """Обработка текстового запроса пользователем."""
    try:
        if not request.message:
            raise ValueError("Отсутствует текст запроса.")

        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": request.message}
            ],
            stream=False
        )
        

        result = response.choices[0].message.content.strip()
        return result

    except Exception as e:
        logger.exception(f"Ошибка при выполнении запроса: {e}")
        return None