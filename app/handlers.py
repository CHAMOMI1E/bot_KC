from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from decorators import check_admin

from config import ADMIN

from app.views import *

import keyboard as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id in ADMIN:
        pass  # TODO написать функцию которую будет возращать клавиатуру админа и отвечать ей за работу админа и тд.
    else:
        await hello(message)


@router.message(F.text == "Просмотр")
async def list_users(message: Message):
    await message.answer("Список юзеров", reply_markup=await kb.main_keyboard())
