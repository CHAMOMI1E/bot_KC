from app.core.keyboard import main
from app.core.decorators import check_admin
from app.views.form import *
from aiogram.fsm.context import FSMContext

from app.db.request import *


@check_admin
async def hello(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=main)


async def check_user_in_db(message: types.Message, state: FSMContext):
    if await get_user_by_id(message.from_user.id):
        return await message.answer(f"Ты уже зарегистрирован!")
    else:
        await state.set_state(Form.name)
        await message.answer("Привет. Для начала введи свое имя:")


async def hello_name(message: types.Message, name: str):
    return await message.reply(f"Hello, {name}")
