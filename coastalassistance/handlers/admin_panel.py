from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from misc.maps import start_map
from constants.const_list_added import LIST_PIC_NON_ACTIVATED
from database.main_db import delete_by_id, get_info_if_activated_zero, set_activated_to_one
from misc.location_info import get_location_info
from keyboards.kb.choice import choice
from keyboards.kb.main_menu import main_menu
from keyboards.inkb.inkb_admin import admin_menu, approve_photo_menu
from config import ADMIN_ID
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from misc.bot import bot
from aiogram.enums import ParseMode

router = Router()

admin_id = ADMIN_ID


@router.message(Command("oblako"))
async def send(message: Message):
    if message.chat.type == "private":
        if message.from_user.id == admin_id:
            await message.answer(
                "🎟 Меню администратора: ", reply_markup=await admin_menu()
            )


class help_admin(StatesGroup):
    hlp_id = State()
    hlp_text = State()
    hlp_answer = State()


@router.callback_query(F.data == "/hlp")
async def command_hlp_start(callback: types.CallbackQuery, state: FSMContext):
    if callback.from_user.id == admin_id:
        await callback.message.answer("Введите id юзера")
        await callback.answer()
        await state.set_state(help_admin.hlp_id)


@router.message(help_admin.hlp_id)
async def command_help_id(message: Message, state: FSMContext):
    await state.update_data(hlp_id=message.text)
    await message.answer("Напишите текст ответа:")
    await state.set_state(help_admin.hlp_text)


@router.message(help_admin.hlp_text)
async def command_help_text(message: Message, state: FSMContext):
    await state.update_data(hlp_text=message.text)
    data = await state.get_data()
    hlp_id = data.get("hlp_id")
    hlp_text = data.get("hlp_text")
    await message.answer(
        f"Ваше сообщение пользователю: {hlp_id}\n{hlp_text}\nОтправляем?",
        reply_markup=await choice(),
    )
    await state.set_state(help_admin.hlp_answer)


@router.message(help_admin.hlp_answer)
async def command_help_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    hlp_id = data.get("hlp_id")
    hlp_text = data.get("hlp_text")
    if message.text == "✅ Да":
        try:
            await bot.send_message(
                chat_id=hlp_id, text=f"🔖 Вам ответили на обращение:\n\n{hlp_text}"
            )
            await message.answer(
                "Сообщение успешно отправлено.", reply_markup=await main_menu()
            )
        except Exception as e:
            print(f"Ошибка во время отправки сообщения (обращение) {e}")
            await message.answer(
                "Не удалось отправить сообщение", reply_markup=await main_menu()
            )
    if message.text == "❌ Нет":
        await state.clear()
        await message.answer("❌ Отмена", reply_markup=await main_menu())
    await state.clear()


@router.callback_query(F.data == "admin_load_photos")
async def list_all_photos(callback: types.CallbackQuery):
    user_shores = await get_info_if_activated_zero()
    if not user_shores:
        await callback.answer(
            "❕ Ещё *не добавили* ни одной фотографии пляжа.",
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        for shore in user_shores:
            coordinates = shore[3]
            latitude = coordinates.split(", ")[0]
            longitude = coordinates.split(", ")[1]
            await bot.send_photo(
                chat_id=shore[1],
                photo=shore[2],
                caption=LIST_PIC_NON_ACTIVATED.format(
                    id=shore[0],
                    geo_tag=coordinates,
                    about=shore[4],
                    location=await get_location_info(
                        longitude=longitude, latitude=latitude
                    ),
                    destruction=shore[5],
                    activated="Да" if shore[6] == 1 else "На проверке",
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=await approve_photo_menu(shore[0]),
            )


@router.callback_query(lambda c: c.data and c.data.startswith("remove_"))
async def delete_non_approve_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    id = (callback_query.data.split("_"))[1]
    await delete_by_id(id=int(id))

    await callback_query.message.answer("Успешно удалено.")


@router.callback_query(lambda c: c.data and c.data.startswith("approve_"))
async def approve_non_approve_callback(callback_query: types.CallbackQuery):
    await callback_query.answer()
    id = (callback_query.data.split("_"))[1]
    print(id)
    await set_activated_to_one(id=int(id))
    await start_map()
    await callback_query.message.answer("Успешно добавлено.")
