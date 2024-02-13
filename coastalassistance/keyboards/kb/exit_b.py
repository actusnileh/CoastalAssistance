from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from async_lru import alru_cache


@alru_cache
async def exit() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="❌ Отмена")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


@alru_cache
async def exit_with_no() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="📝 Без описания")

    kb.button(text="❌ Отмена")
    kb.adjust(1, 1)
    return kb.as_markup(resize_keyboard=True)
