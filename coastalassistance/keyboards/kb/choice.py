from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from async_lru import alru_cache


@alru_cache
async def choice() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="✅ Да")
    kb.button(text="❌ Нет")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
