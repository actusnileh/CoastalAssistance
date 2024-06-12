from aiogram.types import ReplyKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from async_lru import alru_cache


@alru_cache
async def main_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="🖼 Добавить")
    kb.button(text="📚 Добавленные")

    kb.button(text="🌊 Что фотографировать?")

    kb.button(text="🗺 Карты", web_app=WebAppInfo(url="https://192.168.31.78:45331/map_with_points.html"))

    kb.button(text="💬 Обращение")
    kb.button(text="⚙️ Настройки")
    kb.adjust(2, 1, 2)
    return kb.as_markup(resize_keyboard=True)
