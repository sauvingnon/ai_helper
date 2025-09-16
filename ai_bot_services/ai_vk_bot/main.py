from vkbottle.bot import Bot, Message
from config import BOT_TOKEN
from logger import logger
from app.handlers import start, set_model, text_handler
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
    environment="ai_vk_bot",
    send_default_pii=False,  # отключаем автоматическую отправку личных данных
    integrations=[sentry_logging]
)

# Создаем бота
bot = Bot(token=BOT_TOKEN)

bot.labeler.load(start.labeler)
bot.labeler.load(set_model.labeler)
bot.labeler.load(text_handler.labeler)

# Запускаем
if __name__ == "__main__":
    logger.info("Бот стартовал.")
    bot.run_forever()
