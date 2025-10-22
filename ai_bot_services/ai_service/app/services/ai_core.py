import io
import base64
from groq import Groq
from config import API_TOKEN
from logger import logger
from app.api.schemas.model_name import AIRequest, speech_to_text_model, AIAudioResponse

# Инициализация клиента
client = Groq(api_key=API_TOKEN)


# --- 🎤 Speech-to-Text ---
async def ai_voice_request(file: io.BytesIO) -> str | None:
    """Распознаёт речь в аудиофайле и возвращает текст."""
    try:
        logger.info(f"Распознавание аудио через модель: {speech_to_text_model}")

        transcription = client.audio.transcriptions.create(
            file=file,
            model=speech_to_text_model,
            response_format="verbose_json",
            language="ru"
        )

        text = transcription.text.strip()
        logger.info("Распознавание выполнено успешно")

        return text or None

    except Exception as e:
        logger.exception(f"Ошибка при распознавании аудио: {e}")
        return None


# --- 💬 Chat LLM ---
async def ai_message_request(request: AIRequest) -> str | None:
    """Обработка текстового запроса пользователем."""
    try:
        if not request.message:
            raise ValueError("Отсутствует текст запроса.")

        logger.info(f"Выполняется чат-запрос к модели {request.model.value}")

        chat_completion = client.chat.completions.create(
            model=request.model.value,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Ты — русскоязычный AI-ассистент. "
                        "Отвечай кратко и по существу, помогай пользователю."
                    ),
                },
                {"role": "user", "content": request.message}
            ],
        )

        result = chat_completion.choices[0].message.content.strip()
        logger.info("Чат-запрос выполнен успешно")

        return result

    except Exception as e:
        logger.exception(f"Ошибка при выполнении запроса к модели: {e}")
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


# --- 🤖 Обработчик голосовых сообщений ---
async def voice_handler(req: AIRequest) -> AIAudioResponse | None:
    """Обрабатывает запрос с аудио: распознаёт → отвечает."""
    if not req.audio_base64:
        raise ValueError("Отсутствует аудио запроса.")

    try:
        # 1️⃣ base64 → BytesIO
        audio_bytes = base64.b64decode(req.audio_base64)
        file = io.BytesIO(audio_bytes)
        file.name = "voice.wav"

        # 2️⃣ Распознаём речь
        text = await ai_voice_request(file)
        if not text or text == "Продолжение следует...":
            return "Не удалось распознать речь."

        # 3️⃣ Подставляем распознанный текст
        req.message = text

        # 4️⃣ Отправляем в LLM
        result = await ai_message_request(req)
        # base64_sound = await get_audio_response(result)
        if not result:
            return "Ошибка при обработке запроса."
        
        response = AIAudioResponse(
            user_msg=text,
            response=result
            # audio_base64=base64_sound
        )

        # 5️⃣ Возвращаем финальный ответ
        return response

    except Exception as e:
        logger.exception(f"Ошибка при обработке голосового запроса: {e}")
        return None
