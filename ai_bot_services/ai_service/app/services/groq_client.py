import io
import base64
from groq import Groq
from config import API_TOKEN_GROQ
from logger import logger
from app.api.schemas.model_name import AIRequest, speech_to_text_model, AIResponse

# Инициализация клиента
client = Groq(api_key=API_TOKEN_GROQ)

# --- 🎤 Speech-to-Text ---
async def ai_voice_request(file: io.BytesIO) -> str | None:
    """Распознаёт речь в аудиофайле и возвращает текст."""
    try:

        transcription = client.audio.transcriptions.create(
            file=file,
            model=speech_to_text_model,
            response_format="verbose_json",
            language="ru"
        )

        text = transcription.text.strip()

        return text or None

    except Exception as e:
        logger.exception(f"Ошибка при распознавании аудио: {e}")
        return None


# --- 💬 Chat LLM ---
async def ai_message_request(messages, model_name: str) -> str | None:
    """Обработка текстового запроса пользователем."""
    try:

        logger.info(f"Выполняется чат-запрос к модели {model_name} в Groq API")

        chat_completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
        )

        result = chat_completion.choices[0].message.content.strip()
        logger.info("Чат-запрос к Groq API выполнен успешно")

        return result

    except Exception as e:
        logger.exception(f"Ошибка при выполнении запроса в Groq API к модели: {e}")
        return None
    

# --- 🔊 Text-to-Speech ---
async def get_audio_response(text: str) -> str | None:
    """Преобразует текст в озвучку (base64)."""
    try:
        logger.info("Озвучивание текста...")

        response = client.audio.speech.create(
            model="playai-tts",
            voice="Fritz-PlayAI",
            input=text,
            response_format="wav"
        )

        audio_bytes = response.read()
        audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

        logger.info("Озвучивание выполнено успешно")
        return audio_b64

    except Exception as e:
        logger.exception(f"Ошибка при озвучивании текста: {e}")
        return None