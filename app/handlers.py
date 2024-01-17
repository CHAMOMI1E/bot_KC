from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from decorators import check_admin
import keyboard as kb

from config import ADMIN

from app.views import *
from app.admin import *

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id in ADMIN:
        await admin_start(message)
    else:
        await hello(message)


@router.message(F.text == "Просмотр")
async def list_users(message: Message):
    await message.answer("Список юзеров", reply_markup=await kb.main_keyboard())
