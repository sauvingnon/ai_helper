# 💡 Все клавиатуры и команды бота
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand

# 📌 Команды, отображаемые в меню Telegram
commands = [
    BotCommand(command="start", description="🏠 Перезапуск"),
    BotCommand(command="set_model", description="🚀 Выбор модели")
]

# 📱 Клавиатура приветствия
start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🤖 Выбрать модель", callback_data="set_model")]
    ]
)