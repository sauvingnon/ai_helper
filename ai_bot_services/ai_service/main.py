from fastapi import FastAPI
from app.api.endpoints import message_chat

app = FastAPI(debug=True)

# Подключаем роутеры
app.include_router(message_chat.router)