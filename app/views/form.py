from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from app.core.keyboard import accept_keyboard
from app.db.request import add_user
from app.utils.states import Form
from app.core.sender import send_accept_message

register_router = Router()


async def register_user(message: types.Message, state: FSMContext) -> Form.name:
    await state.set_state(Form.name)
    await message.answer("Привет. Для начала введите свое имя:")


@register_router.message(Form.name)
async def surname(message: types.Message, state: FSMContext) -> Form.surname:
    await state.update_data(name=message.text)
    await state.set_state(Form.surname)
    await message.answer("А теперь введите свою фамилию:")


@register_router.message(Form.surname)
async def patronymic(message: types.Message, state: FSMContext) -> Form.patronymic:
    await state.update_data(surname=message.text)
    await state.set_state(Form.patronymic)
    await message.answer("А теперь введите своё отчество:")


@register_router.message(Form.patronymic)
async def result(message: types.Message, state: FSMContext) -> str:
    await state.update_data(patronymic=message.text)
    data = await state.get_data()
    # await state.clear()
    await message.answer(f"Имя: {data['name']} \n"
                         f"Фамилия: {data['surname']} \n"
                         f"Отчество: {data['patronymic']} \n"
                         f"Все верно введено?",
                         reply_markup=accept_keyboard
                         )


@register_router.callback_query(F.data == "accept_register", Form.patronymic)
async def confirm_form(message: types.Message, state: FSMContext) -> str:
    data = await state.get_data()
    await state.clear()
    await add_user(data['name'], data['surname'], data['patronymic'], message.from_user.id)
    # await message.edit_text("Confirm")
    await message.answer("Confirm registration")
    await send_accept_message(data['name'], data['surname'], data['patronymic'], message.from_user.id)


@register_router.callback_query(F.data.startswith("accept_register"), Form.patronymic)
async def decline_form(message: types.Message, state: FSMContext) -> Form.name:
    await message.answer("Окей. Тогда введите сове имя снова: ")
    await state.clear()
    await state.set_state(Form.name)
