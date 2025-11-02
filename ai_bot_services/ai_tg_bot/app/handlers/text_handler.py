from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from logger import logger
from app.services.ai_service import ai_service
from app.schemas.ai_service import ModelName, USER_MODELS, AIRequest

# Телеграмм не даст отправить сообщение длиннее этого....
MAX_LEN = 4000

router = Router()

def split_text(text: str):
    for i in range(0, len(text), MAX_LEN):
        yield text[i:i+MAX_LEN]

# Обработка запроса к модели
@router.message(F.text)
async def text_handler(message: Message, state: FSMContext):
    try:
        model = USER_MODELS.get(message.from_user.id, ModelName.GROQ_PLTF.value)

        message_old = await message.answer("⌛ Запрос принят, обработка…")

        text_message = message.text.strip()

        ai_request = AIRequest(
            user_id=message.from_user.id,
            model=model, 
            message=text_message, 
            audio_base64=None
        )

        logger.info(f"Пользователь {message.from_user.username} с выбранной моделью {model} сделал запрос: {text_message}")

        result = await ai_service.get_answer_for_text(ai_request)

        if result is None:
            raise Exception("Пустой ответ ai_service")
        
        if len(result.response) < MAX_LEN:
            await message_old.edit_text(result.response)
            return
        else:
            await message_old.edit_text("⌛ Ответ большой, делим на части…")
        
        for chunk in split_text(result.response):
            await message_old.answer(chunk)

        logger.info(f"Пользователь {message_old.from_user.username} успешно получил ответ.")

    except Exception as e:
        logger.exception(f"Ошибка обработки запроса от пользователя: {e}")
        await message_old.answer("❌ Произошла ошибка при обработке вашего запроса. Попробуйте снова.")
