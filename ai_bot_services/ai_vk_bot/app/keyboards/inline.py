from vkbottle import Keyboard, KeyboardButtonColor, Text
from app.schemas.ai_service import ModelName

# 📌 Постоянное меню (persistent, будет висеть снизу)
commands = (
    Keyboard(one_time=False, inline=False)
    .add(Text("🏠 Перезапуск", payload={"command": "start"}), color=KeyboardButtonColor.PRIMARY)
    .add(Text("🚀 Выбор модели", payload={"command": "set_model"}), color=KeyboardButtonColor.PRIMARY)
)

# 📱 Клавиатура приветствия (inline, под сообщением)
start_keyboard = (
    Keyboard(inline=True)
    .add(Text("🤖 Выбрать модель", payload={"command": "set_model"}), color=KeyboardButtonColor.PRIMARY)
)

def get_model_keyboard():
    keyboard = Keyboard(inline=True)
    for i, m in enumerate(ModelName, start=1):
        keyboard.add(
            Text(
                label=m.name,
                payload={"command": f"choose_model:{m.value}"}
            )
        )
        if i % 2 == 0:  # каждые 2 кнопки -> новая строка
            keyboard.row()

    keyboard.add(
        Text("❌ Отмена", payload={"command": "cancel_model"}),
        color=KeyboardButtonColor.NEGATIVE
    )

    return keyboard