from vkbottle.bot import BotLabeler, Message, MessageEvent, rules
from app.schemas.ai_service import ModelName, USER_MODELS, MODEL_CONFIG
from logger import logger
from app.keyboards.inline import get_model_keyboard
from vkbottle.dispatch.rules import ABCRule

labeler = BotLabeler()

def get_model_description() -> str:
    lines = ["📖 Доступные модели:\n"]
    for model, info in MODEL_CONFIG.items():
        block = (
            f"🔹 {model.value}\n"
            f"   ├ Роль: {info.role}\n"
            f"   ├ Скорость: {info.speed}\n"
            f"   ├ Качество: {info.quality}\n"
            f"   └ {info.notes}\n"
        )
        lines.append(block)
    return "\n".join(lines)

# ---------------- Хэндлеры ----------------

# ❌ Отмена выбора модели (текст + payload)
@labeler.message(payload={"command": "cancel_model"})
async def cmd_cancel_model(obj):
    user_id = obj.from_id
    value = USER_MODELS.get(user_id, ModelName.LLAMA3_1_8B.value)
    await obj.answer(f"Окей, оставляем тебе {value}. Он тебя слушает 🙂")

# 🚀 Команда "Выбрать модель" (текст + кнопка)
@labeler.message(payload={"command": "set_model"})
async def cmd_set_model(message: Message):
    logger.info("Команда выбрать модель запущена")
    await message.answer(
        f"{get_model_description()}\n\nВыбери модель:",
        keyboard=get_model_keyboard().get_json()
    )

# Правило для обработки выбора модели
class ChooseModelRule(ABCRule[Message]):
    async def check(self, message: Message):
        payload = message.get_payload_json()
        if payload is None:
            return False
        param = payload['command']
        if param and param.startswith("choose_model:"):
            return {"model_value": param.split(":", 1)[1]}
        return False

# Обработка выбора модели
@labeler.message(ChooseModelRule())
async def choose_model_handler(message: Message, model_value: str):
    USER_MODELS[message.from_id] = model_value
    logger.info(f"Пользователь сменил модель на {model_value}")
    await message.answer(f"✅ Модель установлена: {model_value}. Можешь писать свой запрос.")