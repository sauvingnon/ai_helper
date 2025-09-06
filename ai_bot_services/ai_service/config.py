import os
from dotenv import load_dotenv
from pathlib import Path

# Загружаем переменные окружения из .env файла
# load_dotenv()
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Теперь можешь обращаться к переменным окружения
API_TOKEN = os.getenv("API_TOKEN")