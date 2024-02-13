from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from async_lru import alru_cache


@alru_cache
async def help_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="💬 Обращение в поддержку", callback_data="help_send")
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)
