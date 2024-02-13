from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from async_lru import alru_cache


@alru_cache
async def admin_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🔖 Обращения", callback_data="/hlp")

    kb.button(text="🖼 Просмотр всех фотографий", callback_data="admin_load_photos")

    kb.button(text="#️⃣ Редактирование по номеру", callback_data="admin_load_photo")

    kb.adjust(1, 1, 1)
    return kb.as_markup(resize_keyboard=True)


@alru_cache
async def approve_photo_menu(id) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="🟢 Разрешить", callback_data=f"approve_{id}")
    kb.button(text="🔴 Удалить", callback_data=f"remove_{id}")

    kb.adjust(1, 1)
    return kb.as_markup(resize_keyboard=True)
