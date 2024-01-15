from aiogram import types

from decorators import check_admin


@check_admin
async def hello(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")