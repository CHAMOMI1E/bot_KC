from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from app.utils.states import Form

register_router = Router()


async def register_user(message: types.Message, state: FSMContext):
    await state.set_state(Form.name)
    await message.answer("Привет. Для начала введи свое имя:")


@register_router.message(Form.name)
async def surname(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Form.surname)
    await message.answer("А теперь введи свою фамилию:")


@register_router.message(Form.surname)
async def patronymic(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(Form.patronymic)
    await message.answer("А теперь введи своё отчество:")


@register_router.message(Form.patronymic)
async def result(message: types.Message, state: FSMContext):
    await state.update_data(patronymic=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(f"Имя:{data['name']} \n"
                         f"Фамилия: {data['surname']} \n"
                         f"Отчество: {data['patronymic']} \n",
                         )
