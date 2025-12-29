import base64
import io
from app.core.context_manager import ContextManager
from config import MAX_CONTEXT_MESSAGES
from app.api.schemas.model_name import AIRequest, AIResponse
from app.services import groq_client, deepseek_client
from logger import logger

ctx_manager = ContextManager(max_messages=MAX_CONTEXT_MESSAGES)

async def process_message(request: AIRequest) -> AIResponse | None:
    """
    message_type: 'text' | 'voice'
    content: str (text) | path to audio file
    """
    try:
        logger.info(f"Поступил запрос от пользователя {request.user_id}")
        # если гс → распознаём
        if request.audio_base64:
            logger.info(f"Голосовое сообщение получено.")
            audio_bytes = base64.b64decode(request.audio_base64)
            file = io.BytesIO(audio_bytes)
            file.name = "voice.wav"
            text = await groq_client.ai_voice_request(file)
            logger.info(f"Голосовое сообщение успешно обработано.")
            if not text:
                raise ValueError("Не удалось обработать голосовое сообщение")
        else:
            logger.info(f"Текстовое сообщение получено.")
            text = request.message

        user_id = request.user_id

        ctx_manager.add(user_id, "user", text)
        messages = ctx_manager.get_messages(user_id)

        # пробуем groq, fallback → deepseek
        try:
            logger.info(f"Отправка запроса к groq API: {text}")
            reply = await groq_client.ai_message_request(messages, request.model.value)
            if reply is None:
                raise ValueError("Пустой ответ groq API")
            logger.info("Запрос успешно обработан groq API")
        except Exception:
            try:
                logger.info(f"Отправка запроса к deepseek API: {text}")
                reply = await deepseek_client.ai_message_request(messages)
                logger.info("Запрос успешно обработан deepseek API")
            except Exception:
                raise ValueError("Не удалсь выполнить запрос.")

        ctx_manager.add(user_id, "assistant", reply)
        return AIResponse(
            user_msg=text,
            response=reply,
            audio_base64=None
        )

    except Exception as e:
        logger.exception(f"Ошибка: {e}")
        return None
