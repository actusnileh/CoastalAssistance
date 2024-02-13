from aiogram import Router, F
from aiogram.types import Message
from misc.location_info import get_location_info
from constants.const_general import SQL_ERROR
from database.main_db import sql_get_user_shores
from constants.const_list_added import LIST_ADDED_TEXT, LIST_PIC, NO_LIST_ADDED
from aiogram.enums import ParseMode
from misc.bot import bot

router = Router()


@router.message(F.text == LIST_ADDED_TEXT)
async def list_added(message: Message):
    user_id = message.from_user.id
    try:
        user_shores = await sql_get_user_shores(user_id)
    except Exception as e:
        await message.answer(SQL_ERROR, parse_mode=ParseMode.MARKDOWN)
        print(f"Ошибка при выводе всех берегов пользователя в БД {e}")
    else:
        if not user_shores:
            await message.answer(NO_LIST_ADDED, parse_mode=ParseMode.MARKDOWN)
        else:
            for shore in user_shores:
                coordinates = shore[3]
                latitude = coordinates.split(", ")[0]
                longitude = coordinates.split(", ")[1]
                await bot.send_photo(
                    chat_id=shore[1],
                    photo=shore[2],
                    caption=LIST_PIC.format(
                        geo_tag=coordinates,
                        about=shore[4],
                        location=await get_location_info(
                            longitude=longitude, latitude=latitude
                        ),
                        destruction=shore[5],
                        activated="Да" if shore[6] == 1 else "На проверке",
                    ),
                    parse_mode=ParseMode.MARKDOWN,
                )
