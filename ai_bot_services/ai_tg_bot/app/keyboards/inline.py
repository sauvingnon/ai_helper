# 💡 Все клавиатуры и команды бота
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand
from app.schemas.ai_service import ModelName, USER_MODELS

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

def get_model_keyboard(tg_id: int):
    buttons = []
    current_model = USER_MODELS.get(tg_id, ModelName.GROQ_PLTF.value)
    
    # каждая кнопка — в отдельной строке
    for model in ModelName:
        text = f"✅ {model.name}" if model.value == current_model else model.name
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"set_model:{model.value}")])
    
    # добавляем строку с кнопкой отмены
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_model")])
    
    return InlineKeyboardMarkup(inline_keyboard=buttons)