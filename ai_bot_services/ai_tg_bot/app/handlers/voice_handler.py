from aiogram import Router
from aiogram.types import Message, FSInputFile, BufferedInputFile
from logger import logger
from app.services.ai_service import ai_service
from app.utils.convert import convert_with_ffmpeg
import io, base64
from app.schemas.ai_service import USER_MODELS, ModelName, AIRequest

router = Router()

MAX_LEN = 4000

def split_text(text: str):
    for i in range(0, len(text), MAX_LEN):
        yield text[i:i+MAX_LEN]

@router.message(lambda msg: msg.voice)
async def handle_audio(msg: Message):

    try:

        logger.info(f"Пользователь {msg.from_user.username} отправил голосовое сообщение.")

        message_old = await msg.answer("⌛ Запрос принят, обработка…")
        file_obj = msg.voice
        file = await msg.bot.get_file(file_obj.file_id)
        # качаем как байты
        bio = await msg.bot.download_file(file.file_path)
        ogg_bytes = bio.read()

        mp3_bytes = await convert_with_ffmpeg(ogg_bytes)

        if(len(mp3_bytes) == 0):
            raise Exception("Файл пуст")
        
        audio_base64 = base64.b64encode(mp3_bytes).decode("utf-8")

        model = USER_MODELS.get(msg.from_user.id, ModelName.GROQ_PLTF.value)

        request = AIRequest(
            model=model,
            message=None,
            audio_base64=audio_base64
        )

        # отправляем в микросервис
        result = await ai_service.get_answer_for_audio(request)

        if result is None:
            raise Exception("Пустой ответ ai_service")

        await message_old.edit_text(f"Вопрос: {result.user_msg}")

        # if result.audio_base64:
        #     audio_bytes = base64.b64decode(result.audio_base64)
        #     voice = BufferedInputFile(audio_bytes, filename="response.wav")
        #     await msg.bot.send_voice(msg.chat.id, voice)
        
        if len(result.response) < MAX_LEN:
            await message_old.answer(result.response)
        else:
            await message_old.answer("⌛ Ответ большой, делим на части…")
            for chunk in split_text(result.response):
                await message_old.answer(chunk)

        logger.info(f"Пользователь {message_old.from_user.username} успешно получил ответ.")

    except Exception as e:
        logger.exception(f"Ошибка обработки запроса от пользователя: {e}")
        await message_old.answer("❌ Произошла ошибка при обработке вашего запроса. Попробуйте снова.")

    