from aiogram import Router, F
from aiogram.types import Message
from misc.location_info import get_location_info
from constants.const_general import SQL_ERROR
from database.repositories.shore import user_shores
from constants.const_list_added import LIST_ADDED_TEXT, LIST_PIC, NO_LIST_ADDED
from aiogram.enums import ParseMode
from misc.bot import bot

router = Router()


@router.message(F.text == LIST_ADDED_TEXT)
async def list_added(message: Message):
    user_id = message.from_user.id
    try:
        shores = await user_shores(user_id)
    except Exception as e:
        await message.answer(SQL_ERROR, parse_mode=ParseMode.MARKDOWN)
        print(f"Ошибка при выводе всех берегов пользователя в БД {e}")
    else:
        if not shores:
            await message.answer(NO_LIST_ADDED, parse_mode=ParseMode.MARKDOWN)
        else:
            for shore in shores:
                coordinates = shore.geo_tag
                latitude = coordinates.split(", ")[0]
                longitude = coordinates.split(", ")[1]
                await bot.send_photo(
                    chat_id=shore.user_id,
                    photo=shore.photo,
                    caption=LIST_PIC.format(
                        geo_tag=coordinates,
                        about=shore.about,
                        location=await get_location_info(
                            longitude=longitude, latitude=latitude
                        ),
                        destruction=shore.destruction,
                        activated="Да" if shore.activated == 1 else "На проверке",
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
