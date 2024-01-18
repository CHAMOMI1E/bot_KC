from aiogram import types

from app.keyboard import main
from app.decorators import check_admin
from app.views.form import *

from app.db.models import Users, Accounts, async_session
from app.db.request import *


@check_admin
async def hello(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=main)


async def check_user_in_db(message: types.Message):
    if await get_user_by_id(message.from_user.id):
        return await message.answer(f"Ты уже зарегистрирован!")
    else:
        await message.answer(f"Привет. Для начала отправь своё имя:")
        await ProfileStatesGroup.name.set()


async def hello_name(message: types.Message, name: str):
    return await message.reply(f"Hello, {name}")
