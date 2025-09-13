from vkbottle.bot import BotLabeler, Message, MessageEvent
from vkbottle import Keyboard, KeyboardButtonColor, Callback
from app.schemas.ai_service import ModelName, USER_MODELS, MODEL_CONFIG
from typing import Union

chat_labeler = BotLabeler()

# ---------------- Клавиатуры ----------------

def get_model_keyboard():
    keyboard = Keyboard(one_time=True, inline=True)
    for m in ModelName:
        keyboard.add(
            Callback(
                label=m.name,
                payload={"command": f"choose_model:{m.value}"}
            )
        )
    keyboard.row()
    keyboard.add(
        Callback("❌ Отмена", payload={"command": "cancel_model"}),
        color=KeyboardButtonColor.NEGATIVE
    )
    return keyboard

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
@chat_labeler.message(text="/cancel_model")
async def cmd_cancel_model(obj):
    user_id = obj.from_id
    value = USER_MODELS.get(user_id, ModelName.LLAMA3_1_8B.value)
    await obj.answer(f"Окей, оставляем тебе {value}. Он тебя слушает 🙂")

# 🚀 Команда "Выбрать модель" (текст + кнопка)
@chat_labeler.message(text="/set_model")
async def cmd_set_model(obj):
    await obj.answer(
        f"{get_model_description()}\n\nВыбери модель:",
        keyboard=get_model_keyboard().get_json()
    )

# ---------------- Универсальное правило для выбора модели ----------------

class ChooseModelRule(ABCRule[Union[Message, MessageEvent]]):
    """Ловит текстовую команду /choose_model <model> и inline-кнопку choose_model:<model>"""

    async def check(self, obj) -> bool:
        # 1️⃣ payload с кнопки
        payload_command = getattr(obj, "payload", {}).get("command") if hasattr(obj, "payload") else None
        if payload_command and payload_command.startswith("choose_model:"):
            return True

        # 2️⃣ текстовая команда
        text = getattr(obj, "text", "")
        if text.startswith("/choose_model"):
            return True

        return False

# ✅ Пользователь выбрал модель
@chat_labeler.message(ChooseModelRule())
async def choose_model(obj):
    # Получаем модель
    if hasattr(obj, "payload") and obj.payload:
        model_value = obj.payload["command"].split(":", 1)[1]
    else:
        parts = obj.text.split(" ", 1)
        model_value = parts[1] if len(parts) > 1 else "LLAMA3_1_8B"

    USER_MODELS[obj.from_id] = model_value
    await obj.answer(f"✅ Модель установлена: {model_value}. Можете писать свой запрос.")
