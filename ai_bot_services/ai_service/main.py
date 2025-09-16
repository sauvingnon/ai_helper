# Входная точка сервиса по перенаправлению запросов на API сторонних моделей.
from fastapi import FastAPI
from app.api.endpoints import message_chat

# Создаем приложение
app = FastAPI(debug=True)

# Подключаем роутеры
app.include_router(message_chat.router)