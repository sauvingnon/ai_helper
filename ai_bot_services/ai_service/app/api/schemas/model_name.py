from enum import Enum
from typing import Optional
from pydantic import BaseModel

class ModelName(str, Enum):
    GROQ_PLTF = "groq/compound"
    LLAMA3_1_8B = "llama-3.1-8b-instant"
    LLAMA3_3_70B = "llama-3.3-70b-versatile"
    GEMMA2_9B = "gemma2-9b-it"
    DEEPSEEK_R1_70B = "deepseek-r1-distill-llama-70b"
    QWEN3_32B = "qwen/qwen3-32b"
    MOONSHOT_KIMI_K2 = "moonshotai/kimi-k2-instruct"


class ModelInfo:
    def __init__(self, role: str, speed: str, quality: str, notes: Optional[str] = None):
        self.role = role          # основная задача модели
        self.speed = speed        # скорость (иконки для наглядности)
        self.quality = quality    # качество
        self.notes = notes or ""  # доп. описание


MODEL_CONFIG: dict[ModelName, ModelInfo] = {
    ModelName.GROQ_PLTF: ModelInfo(
        "⚙️ Универсальный чат без лимита",
        "⚡",
        "среднее",
        "Подходит для любых задач, дешёвый и быстрый. Можно юзать, когда неважно качество, а нужен просто ответ."
    ),
    ModelName.LLAMA3_1_8B: ModelInfo(
        "💬 Быстрый чат",
        "⚡⚡",
        "среднее",
        "Хорошо для повседневных диалогов, быстрых вопросов. Дешёвый, мгновенно отвечает, но иногда тупит."
    ),
    ModelName.LLAMA3_3_70B: ModelInfo(
        "🧠 Глубокий ассистент",
        "🐢",
        "максимум",
        "Подходит для серьёзных задач: рассуждения, сложные ответы, длинные тексты. Медленный, но умный."
    ),
    ModelName.GEMMA2_9B: ModelInfo(
        "📝 Генерация текста",
        "⚡",
        "высокое",
        "Оптимальный вариант для статей, описаний, постов. Баланс скорости и качества."
    ),
    ModelName.DEEPSEEK_R1_70B: ModelInfo(
        "👨‍💻 Кодинг / логика",
        "🐢",
        "очень высокое",
        "Лучшая для программирования и логических задач. Может писать сложный код и объяснять алгоритмы."
    ),
    ModelName.QWEN3_32B: ModelInfo(
        "🔧 Код + аналитика",
        "⚡",
        "высокое",
        "Тоже хороша в коде, но быстрее чем DeepSeek. Можно юзать, если нужен баланс между скоростью и качеством."
    ),
    ModelName.MOONSHOT_KIMI_K2: ModelInfo(
        "🚀 Эксперименты / reasoning",
        "⚡",
        "высокое",
        "Интересная экспериментальная модель. Хороша в рассуждениях, но нестабильна. Можно пробовать для идей."
    ),
}


class AIRequest(BaseModel):
    model: ModelName
    message: str


def get_model_description() -> str:
    """Возвращает текстовое описание всех моделей"""
    text = "📖 Доступные модели:\n\n"
    for model, info in MODEL_CONFIG.items():
        text += (
            f"**{model.value}**\n"
            f"Роль: {info.role}\n"
            f"Скорость: {info.speed}\n"
            f"Качество: {info.quality}\n"
            f"{info.notes}\n\n"
        )
    return text
