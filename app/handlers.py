from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

import keyboard as kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")


@router.message(F.text == "Просмотр")
async def list_users(message: Message):
    await message.answer("Список юзеров", reply_markup=await kb.main_keyboard())
