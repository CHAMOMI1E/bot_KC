from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


register_router = Router()


class ProfileStatesGroup(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()


@register_router.message(ProfileStatesGroup.name)
async def name(message: types.Message):
    pass