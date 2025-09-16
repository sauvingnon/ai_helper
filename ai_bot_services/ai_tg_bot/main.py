import asyncio
from aiogram import Bot, Dispatcher, types
from config import BOT_TOKEN
from app.dispatcher_module import setup_routers
from aiogram.fsm.storage.memory import MemoryStorage
from logger import logger
from app.keyboards.inline import commands
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
    environment="ai_tg_bot",
    send_default_pii=False,  # отключаем автоматическую отправку личных данных
    integrations=[sentry_logging]
)

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=BOT_TOKEN)

async def main():
    logger.info("Бот запущен.")
    await bot.set_my_commands(commands)
    setup_routers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
