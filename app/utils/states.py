from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()


class Post(StatesGroup):
    text = State()
