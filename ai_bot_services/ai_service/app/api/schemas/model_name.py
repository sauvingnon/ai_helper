from enum import Enum
from typing import Optional
from pydantic import BaseModel

speech_to_text_model = "whisper-large-v3-turbo"

# Типы моделей
class ModelName(str, Enum):
    # Бесплатно вроде
    GROQ_PLTF = "groq/compound"
    # Попроще
    LLAMA3_3_70B = "llama-3.3-70b-versatile"
    # Получше
    LLAMA_MAVERICK = "meta-llama/llama-4-maverick-17b-128e-instruct"
    # Квен - просто так
    QWEN3_32B = "qwen/qwen3-32b"
    # Топ вроде как из всех
    GPT_OSS_120B = "openai/gpt-oss-120b"

class AIAudioResponse(BaseModel):
    user_msg: str
    response: str
    audio_base64: Optional[str] = None

class ModelInfo:
    def __init__(self, role: str, speed: str, quality: str, notes: Optional[str] = None):
        self.role = role          # основная задача модели
        self.speed = speed        # скорость (иконки для наглядности)
        self.quality = quality    # качество
        self.notes = notes or ""  # доп. описание

# Вариации моделей и их описания
MODEL_CONFIG: dict[ModelName, ModelInfo] = {
    ModelName.GROQ_PLTF: ModelInfo(
        "⚙️ Универсальный чат с доступом к инструментам",
        "⚡⚡",
        "высокое",
        "Бесплатный или низкозатратный вариант. Compound Beta сочетает LLM + web search и инструменты под капотом. Отлично подходит для ассистента с живым поиском и кодом, без лимитов на токены."
    ),

    ModelName.LLAMA3_3_70B: ModelInfo(
        "⚙️ Мощная текстовая LLM для диалогов и анализа",
        "⚡⚡",
        "высокое",
        "70B параметров, контекст 131k токенов, только текст. Отлично подходит для чат-ботов, анализа текста и кода. Быстрее и проще в инференсе, чем Llama 4 Maverick, мультимодальности нет."
    ),

    ModelName.LLAMA_MAVERICK: ModelInfo(
        "🖼️ Мультимодальная LLM с экспертной архитектурой MoE",
        "⚡⚡⚡",
        "очень высокое",
        "17B активных параметров, 128 экспертов, контекст 131k токенов, мультимодальная (текст + изображения). Отлично подходит для сложных ассистентов, анализа длинных диалогов и визуального контента. Требует больше ресурсов."
    ),

    ModelName.QWEN3_32B: ModelInfo(
        "⚡ Современная LLM для текстового анализа",
        "⚡⚡",
        "высокое",
        "32B параметров, контекст 40k токенов. Хорошо справляется с текстовыми задачами и извлечением информации. Не мультимодальная, не имеет встроенного интернет-доступа, но стабильная и надёжная для NLP-задач."
    ),

    ModelName.GPT_OSS_120B: ModelInfo(
        "⚡ Огромная открытая LLM с высокой reasoning способностью",
        "⚡⚡⚡",
        "очень высокое",
        "120B параметров, контекст 131k токенов, только текст. Отлично подходит для сложных reasoning задач, кодирования, анализа текста. Не имеет встроенного интернет-доступа, требует мощной инфраструктуры для инференса."
    ),

}

# Схема запроса
class AIRequest(BaseModel):
    model: ModelName
    message: Optional[str] = None
    audio_base64: Optional[str] = None

# Для возвращения описания моделей.
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
