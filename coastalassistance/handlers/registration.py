import re
from aiogram import Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.kb.main_menu import main_menu
from keyboards.kb.choice import choice

from constants.const_general import ADD_USER_SQL_ERROR, CHOICE_DESIRED
from constants.const_registration import (
    ALDREADY_EXIST_REGISTER_CANCELLED,
    SUCCESSFUL_REGISTER,
    USER_ALREADY_EXIST,
)

from database.main_db import sql_add_user, sql_check_exist_user, sql_update_user_name

router = Router()


class Registration(StatesGroup):
    confirmation = State()


@router.message(Command(commands=["start"]))
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_name = message.from_user.username

    if await sql_check_exist_user(user_id):
        await message.answer(USER_ALREADY_EXIST, reply_markup=await choice())
        await state.set_state(Registration.confirmation)
    else:
        try:
            await sql_add_user(user_id)
        except Exception as e:
            await message.answer(ADD_USER_SQL_ERROR)
            print(f"Ошибка при добавлении пользователя в БД: {e}")
        else:
            await sql_update_user_name(user_name, user_id)
            await message.answer(
                SUCCESSFUL_REGISTER.format(first_name=user_first_name),
                reply_markup=await main_menu(),
            )
            await state.clear()


@router.message(Registration.confirmation)
async def registration_confirmation(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_name = message.from_user.username

    answer = message.text.lower()
    if re.search(r"да", answer, re.IGNORECASE):
        try:
            await sql_add_user(user_id=user_id)
        except Exception as e:
            await message.answer(ADD_USER_SQL_ERROR)
            print(f"Ошибка при добавлении пользователя в БД: {e}")
        else:
            await sql_update_user_name(user_name, user_id)
            await state.clear()
            await message.answer(
                SUCCESSFUL_REGISTER.format(first_name=user_first_name),
                reply_markup=await main_menu(),
            )
    elif re.search(r"нет", answer, re.IGNORECASE):
        await message.answer(
            ALDREADY_EXIST_REGISTER_CANCELLED, reply_markup=await main_menu()
        )
        await state.clear()
    else:
        await message.answer(CHOICE_DESIRED, reply_markup=await choice())
