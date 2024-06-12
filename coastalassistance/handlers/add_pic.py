import os
from aiogram import Router, F
from misc.maps import start_map
from neural_networks.load_model import check_prediction
from database.repositories.shore import add_shores
from keyboards.kb.main_menu import main_menu
from constants.const_addpic import (
    ADD_PIC_ERROR,
    ADD_PIC_ERROR_INT_DESTRUCTION,
    ADD_PIC_NOT_COASTAL,
    ADD_PIC_READY,
    ADD_PIC_SEND_ABOUT,
    ADD_PIC_SEND_ABOUT_ERROR,
    ADD_PIC_SEND_DESTRUCTION,
    ADD_PIC_SEND_GEO_TAG,
    ADD_PIC_SEND_GEO_TAG_ERROR,
    ADD_PIC_SEND_PHOTO,
    ADD_PIC_SEND_PHOTO_ERROR,
    ADD_PIC_TEXT,
)
from aiogram.types import Message
from aiogram.enums import ParseMode
from keyboards.kb.exit_b import exit, exit_with_no
from aiogram.fsm.state import StatesGroup, State
from misc.bot import bot
from aiogram.fsm.context import FSMContext

router = Router()


class AddPicture(StatesGroup):
    load_image = State()
    geo_tag = State()
    about = State()
    destruction = State()


@router.message(F.text == ADD_PIC_TEXT)
async def add_pic(message: Message, state: FSMContext):
    await message.answer(
        ADD_PIC_SEND_PHOTO, parse_mode=ParseMode.MARKDOWN, reply_markup=await exit()
    )
    await state.set_state(AddPicture.load_image)


@router.message(AddPicture.load_image)
async def question_load_pic(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("❌ Отмена", reply_markup=await main_menu())
    elif message.photo:
        photo = message.photo[-1].file_id
        await bot.download(
            message.photo[-1], destination=f"./img/{message.photo[-1].file_id}.jpg"
        )

        image_path = f"./img/{message.photo[-1].file_id}.jpg"
        await state.update_data(photo=photo)
        is_prediction_ok = await check_prediction(image_path)
        os.remove(image_path)
        if is_prediction_ok:
            await message.answer(
                ADD_PIC_SEND_GEO_TAG,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=await exit(),
            )
            activated = 1
            await state.update_data(activated=activated)
            await state.set_state(AddPicture.geo_tag)
        else:
            await message.answer(
                ADD_PIC_NOT_COASTAL,
                reply_markup=await exit(),
                parse_mode=ParseMode.MARKDOWN,
            )
            activated = 0
            await state.update_data(activated=activated)
            await state.set_state(AddPicture.geo_tag)
    else:
        await message.answer(ADD_PIC_SEND_PHOTO_ERROR, parse_mode=ParseMode.MARKDOWN)
        await state.set_state(AddPicture.load_image)


@router.message(AddPicture.geo_tag)
async def location_load_pic(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("❌ Отмена", reply_markup=await main_menu())
    elif message.location:
        geo_tag = "{}, {}".format(message.location.latitude, message.location.longitude)
        await state.update_data(geo_tag=geo_tag)
        await message.answer(
            ADD_PIC_SEND_DESTRUCTION,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=await exit(),
        )
        await state.set_state(AddPicture.destruction)
    else:
        await message.answer(ADD_PIC_SEND_GEO_TAG_ERROR, parse_mode=ParseMode.MARKDOWN)
        await state.set_state(AddPicture.geo_tag)


@router.message(AddPicture.destruction)
async def destruction_load_pic(message: Message, state: FSMContext):
    if message.text == "❌ Отмена":
        await state.clear()
        await message.answer("❌ Отмена", reply_markup=await main_menu())
    elif message.text:
        try:
            answer = int(message.text)
            if not 0 <= answer <= 100:
                raise ValueError
        except ValueError:
            await message.answer(
                ADD_PIC_ERROR_INT_DESTRUCTION,
                reply_markup=await exit(),
                parse_mode=ParseMode.MARKDOWN,
            )
            await state.set_state(AddPicture.destruction)
        else:
            destruction = answer
            await state.update_data(destruction=destruction)
            await message.answer(
                ADD_PIC_SEND_ABOUT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=await exit_with_no(),
            )
            await state.set_state(AddPicture.about)
    else:
        await message.answer(ADD_PIC_SEND_GEO_TAG_ERROR, parse_mode=ParseMode.MARKDOWN)
        await state.set_state(AddPicture.geo_tag)


@router.message(AddPicture.about)
async def about_load_pic(message: Message, state: FSMContext):
    if message.text:
        if message.text == "❌ Отмена":
            await state.clear()
            await message.answer("❌ Отмена", reply_markup=await main_menu())
        if message.text == "📝 Без описания":
            about = "Без описания"
        else:
            about = message.text

        shore_data = await state.get_data()

        shore_photo = shore_data["photo"]
        shore_geo_tag = shore_data["geo_tag"]
        shore_activated = shore_data["activated"]
        shore_destruction = shore_data["destruction"]

        try:
            await add_shores(
                user_id=message.from_user.id,
                photo=shore_photo,
                geo_tag=shore_geo_tag,
                about=about,
                destruction=shore_destruction,
                activated=shore_activated,
            )
        except Exception as e:
            await message.answer(
                ADD_PIC_ERROR.format(error=e), parse_mode=ParseMode.MARKDOWN
            )
            print(f"Ошибка при добавлении берега в БД {e}")
        else:
            await message.answer_photo(
                photo=shore_photo,
                caption=ADD_PIC_READY.format(
                    geo_tag=shore_geo_tag, about=about, destruction=shore_destruction
                ),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=await main_menu(),
            )
            await start_map()
            await state.clear()
    else:
        await message.answer(ADD_PIC_SEND_ABOUT_ERROR, parse_mode=ParseMode.MARKDOWN)
        await state.set_state(AddPicture.about)
