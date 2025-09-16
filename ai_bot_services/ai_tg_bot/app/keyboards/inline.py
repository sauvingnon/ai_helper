# 💡 Все клавиатуры и команды бота
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from app.schemas.ai_service import ModelName

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

def get_model_keyboard():
    buttons = [
        [InlineKeyboardButton(text=m.name, callback_data=f"set_model:{m.value}")]
        for m in ModelName
    ]
    # Добавляем отдельную строку для кнопки "Отмена"
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_model")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)