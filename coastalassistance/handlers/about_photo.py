from aiogram import Router, F
from aiogram.types import Message
from keyboards.kb.main_menu import main_menu
from aiogram.enums import ParseMode

from constants.const_about_photo import ABOUT_PHOTO_TEXT, BUTTON_WHAT_PHOTO

router = Router()


@router.message(F.text == BUTTON_WHAT_PHOTO)
async def about_photo(message: Message):
    await message.answer(
        ABOUT_PHOTO_TEXT, reply_markup=await main_menu(), parse_mode=ParseMode.MARKDOWN
    )
