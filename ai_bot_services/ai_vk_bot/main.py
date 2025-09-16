from vkbottle.bot import Bot, Message
from config import BOT_TOKEN
from logger import logger
from app.handlers import start, set_model, text_handler

# Создаем бота
bot = Bot(token=BOT_TOKEN)

bot.labeler.load(start.labeler)
bot.labeler.load(set_model.labeler)
bot.labeler.load(text_handler.labeler)

# Запускаем
if __name__ == "__main__":
    logger.info("Бот стартовал.")
    bot.run_forever()
