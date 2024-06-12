from aiogram import Bot, Dispatcher
from config import settings

bot = Bot(token=settings.bot_token)
dp = Dispatcher()
