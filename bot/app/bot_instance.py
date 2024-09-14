from aiogram import Bot

from bot.app.config import settings


bot = Bot(
    token=settings.BOT_TOKEN
)
