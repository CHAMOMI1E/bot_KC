from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from manage import dp


class ProfileStatesGroup(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()


@dp.message_handler(content_types=['name'], state=ProfileStatesGroup.name)
async def add_name(message: types.Message, state: FSMContext) -> None:


    await message.answer("Введите фамилию:")
    await ProfileStatesGroup.next()

@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.name)
async def add_name(message: types.Message, state: FSMContext):
    # Получаем текст сообщения (имя) от пользователя
    name = message.text

    # Сохраняем имя в состоянии
    await state.update_data(name=name)

    # Продолжаем с другими шагами, если необходимо

@dp.message_handler(content_types=['text'], state=ProfileStatesGroup.surname)
async def add_surname(message: types.Message, state: FSMContext):
    # Получаем текст сообщения (фамилия) от пользователя
    surname = message.text

    # Сохраняем фамилию в состоянии
    await state.update_data(surname=surname)

    # Продолжаем с другими шагами, если необходимо

# В другой части кода, где вам нужно использовать сохраненные данные
async def some_other_function(state: FSMContext):
    # Получаем данные из состояния
    state_data = await state.get_data()
    name = state_data.get('name', '')
    surname = state_data.get('surname', '')
    patronymic = state_data.get('patronymic', '')