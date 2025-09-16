from aiogram import Dispatcher
from app.handlers import start, text_handler, set_model

def setup_routers(dp: Dispatcher):
    dp.include_router(set_model.router)
    dp.include_router(start.router)
    dp.include_router(text_handler.router)