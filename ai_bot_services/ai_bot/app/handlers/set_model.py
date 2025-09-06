from aiogram import Router, types, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.state.model_fsm import ModelFSM
from app.schemas.ai_service import ModelName, USER_MODELS, MODEL_CONFIG

router = Router()

def get_model_keyboard():
    buttons = [
        [InlineKeyboardButton(text=m.name, callback_data=f"set_model:{m.value}")]
        for m in ModelName
    ]
    # Добавляем отдельную строку для кнопки "Отмена"
    buttons.append([InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_model")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def get_model_description() -> str:
    """Возвращает текстовое описание всех моделей на основе MODEL_CONFIG"""
    lines = ["📖 Доступные модели:\n"]
    for model, info in MODEL_CONFIG.items():
        block = (
            f"🔹 **{model.value}**\n"
            f"   ├ Роль: {info.role}\n"
            f"   ├ Скорость: {info.speed}\n"
            f"   ├ Качество: {info.quality}\n"
            f"   └ {info.notes}\n"
        )
        lines.append(block)
    return "\n".join(lines)

@router.callback_query(F.data == "cancel_model")
async def cmd_cancel_model_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    value = USER_MODELS.get(callback.from_user.id, ModelName.LLAMA3_1_8B.value)

    await callback.message.answer(f"Окей, оставляем тебе - {value}. Он тебя слушает:")
    await callback.answer()

# Команда /set_model
@router.message(F.text == "/set_model")
async def cmd_set_model_message(message: Message, state: FSMContext):
    await state.set_state(ModelFSM.choosing)
    await message.answer(
        f"{get_model_description()}\n\nВыбери модель:",
        reply_markup=get_model_keyboard()
    )

# Кнопка «Выбрать модель» (callback_data="set_model")
@router.callback_query(F.data == "set_model")
async def cmd_set_model_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ModelFSM.choosing)
    await callback.message.answer(
        f"{get_model_description()}\n\nВыбери модель:",
        reply_markup=get_model_keyboard()
    )
    await callback.answer()  # закрывает «часики» на кнопке

@router.callback_query(F.data.startswith("set_model:"))
async def choose_model(callback: types.CallbackQuery, state: FSMContext):
    model_value = callback.data.split(":", 1)[1]
    USER_MODELS[callback.from_user.id] = model_value
    await state.clear()
    await callback.message.edit_text(f"✅ Модель установлена: {model_value}. Можете писать свой запрос:")
    await callback.answer()
