from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from app.core.keyboard import accept_keyboard, form_accept
from app.db.request import add_user
from app.utils.states import Form
from app.core.sender import send_accept_message

register_router = Router()


async def register_user(message: types.Message, state: FSMContext) -> Form.name:
    await state.set_state(Form.name)
    await message.answer("Привет. Для начала введите свое имя:")


@register_router.message(Form.name)
async def surname(message: types.Message, state: FSMContext) -> Form.surname:
    await state.update_data(name=message.text.title())
    await state.set_state(Form.surname)
    await message.answer("А теперь введите свою фамилию:")


@register_router.message(Form.surname)
async def patronymic(message: types.Message, state: FSMContext) -> Form.patronymic:
    await state.update_data(surname=message.text.title())
    await state.set_state(Form.patronymic)
    await message.answer("А теперь введите своё отчество:")


@register_router.message(Form.patronymic)
async def result(message: types.Message, state: FSMContext) -> str:
    await state.update_data(patronymic=message.text.title())
    data = await state.get_data()
    await state.clear()
    await message.answer(f"Имя: {data['name']} \n"
                         f"Фамилия: {data['surname']} \n"
                         f"Отчество: {data['patronymic']} \n"
                         f"Все верно введено?",
                         reply_markup=form_accept(name=data['name'], surname=data['surname'],
                                                  patronymic=data['patronymic'])
                         )


@register_router.callback_query(F.data.startswith('forma_'))
async def confirm_form(call: types.CallbackQuery) -> str:
    data = call.data.split('_')
    name, surname, patronymic = data[1], data[2], data[3]
    await add_user(name, surname, patronymic, call.from_user.id)
    await call.message.edit_text("Ожидайте подтверждения...")
    await send_accept_message(name, surname, patronymic, call.from_user.id)


@register_router.callback_query(F.data == "form_decline")
async def decline_form(call: types.CallbackQuery, state: FSMContext) -> Form.name:
    await call.message.edit_text("Окей. Тогда введите сове имя снова: ")
    await state.set_state(Form.name)
