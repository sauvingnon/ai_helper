from vkbottle import Keyboard, KeyboardButtonColor, Callback

# 📌 Постоянное меню (persistent, будет висеть снизу)
commands = (
    Keyboard(one_time=False, inline=False)
    .add(Callback("🏠 Перезапуск", payload={"command": "start"}), color=KeyboardButtonColor.PRIMARY)
    .add(Callback("🚀 Выбор модели", payload={"command": "set_model"}), color=KeyboardButtonColor.PRIMARY)
)

# 📱 Клавиатура приветствия (inline, под сообщением)
start_keyboard = (
    Keyboard(one_time=False, inline=True)
    .add(Callback("🤖 Выбрать модель", payload={"command": "set_model"}), color=KeyboardButtonColor.PRIMARY)
)
