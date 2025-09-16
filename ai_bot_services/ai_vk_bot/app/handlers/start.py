from app.utils.resources import get_welcome_message
from app.keyboards.inline import start_keyboard, commands
from vkbottle.bot import BotLabeler, Message
from logger import logger

labeler = BotLabeler()

async def extract_username(api, user_id: int) -> str:
    try:
        user_info = await api.users.get(user_id)
        if user_info and len(user_info) > 0:
            user = user_info[0]
            return f"{user.first_name} {user.last_name}"
    except Exception:
        pass
    return f"Unknown {user_id}"

# Стартовое сообщение
@labeler.message(payload={"command": "start"})
@labeler.message(text=["Начать"])
async def start_handler(message: Message):
    try:
        user_name = await extract_username(message.ctx_api, message.from_id)

        logger.info(f"Пользователь {user_name} запустил бота.")

        await message.answer(
            get_welcome_message(user_name),
            keyboard=commands.get_json()
        )

        await message.answer(
            "Можешь 👉 свой первый запрос или изменить модель:",
            keyboard=start_keyboard.get_json()
        )

    except Exception as e:
        logger.exception(f"Ошибка в /start: {e}")
