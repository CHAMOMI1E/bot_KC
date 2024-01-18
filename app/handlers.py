from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from app import keyboard as kb

from config import ADMIN

from app.views.main_view import *
from app.admin import *

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    # await message.answer(await check_user_in_db(message))
    if message.from_user.id in ADMIN:
        await admin_start(message)
    else:
        await check_user_in_db(message)


@router.message(F.data == "send_text")
async def list_users(message: Message):
    await message.answer("Список юзеров", reply_markup=await kb.main_keyboard())

