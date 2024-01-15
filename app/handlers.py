from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from decorators import check_admin

from app.views import *

import keyboard as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await hello(message)


@router.message(F.text == "Просмотр")
async def list_users(message: Message):
    await message.answer("Список юзеров", reply_markup=await kb.main_keyboard())
