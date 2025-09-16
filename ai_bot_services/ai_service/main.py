# Входная точка сервиса по перенаправлению запросов на API сторонних моделей.
from fastapi import FastAPI
from app.api.endpoints import message_chat
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

# Логи в Sentry
sentry_logging = LoggingIntegration(
    level=None,        # все уровни передаем
    event_level="INFO" # только ошибки будут как события
)

# Подготовка Sentry
sentry_sdk.init(
    dsn="https://1bfb0133d12a1e37c33f022baad9858d@o4509921859076096.ingest.de.sentry.io/4510030089420880",
    environment="ai_service",
    send_default_pii=False,  # отключаем автоматическую отправку личных данных
    integrations=[sentry_logging]
)

# Создаем приложение
app = FastAPI(debug=True)

# Подключаем роутеры
app.include_router(message_chat.router)