import re
from aiogram.enums import ParseMode

from aiogram.types import CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from keyboards.inkb.inkb_admin import admin_menu
from keyboards.kb.main_menu import main_menu
from keyboards.inkb.inkb_help import help_button
from constants.const_help import (
    HELP_COMMAND_TEXT,
    HELP_SEND_ERROR,
    HELP_START_TEXT,
    HELP_TEXT,
    HELP_TEXT_SEND,
)

from keyboards.kb.exit_b import exit

from misc.bot import bot
from config import settings


class Help(StatesGroup):
    help_send = State()


router = Router()


@router.message(F.text == HELP_COMMAND_TEXT)
async def send(message: Message):
    await message.answer(
        HELP_TEXT,
        reply_markup=await help_button(),
        parse_mode=ParseMode.MARKDOWN,
    )


@router.message(F.text == "/help")
async def send_command(message: Message):
    await message.answer(
        HELP_TEXT,
        reply_markup=await help_button(),
        parse_mode=ParseMode.MARKDOWN,
    )


@router.callback_query(F.data == "help_send")
async def command_help_send(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        HELP_START_TEXT,
        reply_markup=await exit(),
    )
    await callback.answer()
    await state.set_state(Help.help_send)


@router.message(Help.help_send)
async def command_help_finish(message: Message, state: FSMContext):
    if re.search(r"отмена", message.text, re.IGNORECASE):
        await state.clear()
        await message.answer("❌ Отмена", reply_markup=await main_menu())
    else:
        await state.update_data(help_send=message.text)
        try:
            await bot.send_message(
                settings.admin_id,
                f"id: {message.from_user.id}\nusername: {message.from_user.username}\n\n{message.text}",
                reply_markup=await admin_menu(),
            )
            await message.answer(
                HELP_TEXT_SEND,
                reply_markup=await main_menu(),
            )
        except Exception as e:
            print(
                f"У пользователя {message.from_user.id} не получилось отправить сообщение {e}"
            )
            await message.answer(
                HELP_SEND_ERROR,
                reply_markup=await main_menu(),
            )
        await state.clear()
