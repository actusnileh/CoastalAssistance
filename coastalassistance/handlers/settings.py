from aiogram import Router, F
from aiogram.types import Message
from aiogram.enums import ParseMode

from database.repositories.user import read_usertype
from database.repositories.shore import read_count_photos

from constants.const_settings import SETTINGS, SETTINGS_TEXT

router = Router()


@router.message(F.text == SETTINGS_TEXT)
async def settings(message: Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    usertype = await read_usertype(user_id)
    count_photos = await read_count_photos(user_id)

    await message.answer(
        SETTINGS.format(
            first_name=first_name, count_photos=count_photos, usertype=usertype
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
