import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Теперь можешь обращаться к переменным окружения
AI_SERVICE_URL = os.getenv("AI_SERVICE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")