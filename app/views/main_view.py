from app.core.keyboard import admin_keyboard
from app.views.form import *
from aiogram.fsm.context import FSMContext

from app.db.request import *
from app.db.models import Status


async def hello(message: types.Message):
    await message.answer(f"Hello, {message.from_user.full_name}!", reply_markup=admin_keyboard())


async def check_user_in_db(message: types.Message, state: FSMContext):
    user = await get_user_by_id_tg(message.from_user.id)
    if user:
        if user.status == Status.ACTIVE.value :
            return await message.answer(f"Вы уже зарегистрированы!")
        elif user.status == Status.DISABLE.value:
            return await message.answer(f"У вас нет прав доступа")
        elif user.status == Status.UNKNOWN.value:
            return await message.answer(f"Ожидайте подтверждения администратора...")

    else:
        await state.set_state(Form.surname)
        await message.answer("Привет. Для начала введите свою фаимилию:")
