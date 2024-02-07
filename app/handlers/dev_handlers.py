from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from app.core.filter.is_admin import IsDeveloper

from app.core.keyboard import dev_keyboard, dev_change
from app.db.request import get_user, get_account
from app.utils.states import Change


dev_router = Router()
dev_router.message.filter(IsDeveloper())


async def dev_start(message: types.Message):
    await message.answer("Здравствуй мой дорогой хозяин!\n"
                         "Отправляю вам вашу рабочую и тестовую клавиатуру!\n"
                         "Чем я могу тебе помочь?",
                         reply_markup=dev_keyboard()
                         )


@dev_router.message(F.text == "Изменить статус пользователя")
async def start_change_status(message: types.Message, state: FSMContext):
    await state.set_state(Change.surname)
    await message.answer("Введите фамилию сотрудника которому надо сменить статус:")


@dev_router.message(Change.surname)
async def confirm_change_status(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    data = await state.get_data()
    await state.clear()
    user = await get_user(surn=data["surname"], action=None)
    if user:
        account = await get_account(user.id)
        await message.answer(f"Фамилия: {user.surname}\n"
                             f"Имя: {user.name}\n"
                             f"Отчество: {user.patronymic}\n"
                             f"Текущий статус: {account.status}\n\n"
                             f"На какой статус надо поменять?", reply_markup=dev_change(id_tg=account.id_tg))
