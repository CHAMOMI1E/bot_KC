from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()


class Post(StatesGroup):
    text = State()


class Delete(StatesGroup):
    surname = State()


class Unblock(StatesGroup):
    surname = State()


class Change(StatesGroup):
    surname = State()


class NewAdmin(StatesGroup):
    surname = State()


class TakeAwayAdmin(StatesGroup):
    surname = State()
