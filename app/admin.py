from aiogram import types

from app.keyboard import main
from app.decorators import check_admin


@check_admin
async def admin_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Ты авторизован(а) как админ", reply_markup=main)


@check_admin
async def admin_show_users(message: types.Message):
    users = ()
    text = "Список сотрудников:/n"
    for user in users:
        text = text + f"{user.name}"

