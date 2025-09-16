from vkbottle.bot import BotLabeler, Message
from logger import logger
from app.services.ai_service import ai_service
from app.schemas.ai_service import ModelName, USER_MODELS, AIRequest

labeler = BotLabeler()

# ВКонтакте тоже есть лимит на длину текста
MAX_LEN = 4000  

def split_text(text: str):
    for i in range(0, len(text), MAX_LEN):
        yield text[i:i + MAX_LEN]


async def extract_username(api, user_id: int) -> str:
    try:
        user_info = await api.users.get(user_id)
        if user_info and len(user_info) > 0:
            user = user_info[0]
            return f"{user.first_name} {user.last_name}"
    except Exception:
        pass
    return f"Unknown {user_id}"

# Обработка запроса
@labeler.message()
async def input_message(message: Message):
    try:
        user_id = message.from_id
        model = USER_MODELS.get(user_id, ModelName.LLAMA3_1_8B.value)

        text_message = message.text.strip()
        user_name = await extract_username(message.ctx_api, user_id)

        ai_request = AIRequest(model=model, message=text_message)

        logger.info(
            f"Пользователь {user_name} с выбранной моделью {model} сделал запрос: {text_message}"
        )

        response = await ai_service.get_answer(ai_request)

        if not response:
            raise Exception("Пустой ответ ai_service")

        if len(response) < MAX_LEN:
            await message.answer(response)
        else:
            await message.answer("⌛ Ответ большой, делим на части…")
            for chunk in split_text(response):
                await message.answer(chunk)

        logger.info(f"Пользователь {user_name} успешно получил ответ.")

    except Exception as e:
        logger.exception(f"Ошибка обработки запроса от пользователя: {e}")
        await message.answer("❌ Произошла ошибка при обработке вашего запроса. Попробуйте снова.")
