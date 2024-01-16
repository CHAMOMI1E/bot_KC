from aiogram import types

from keyboard import main
from decorators import check_admin


@check_admin
async def hello(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=main)
