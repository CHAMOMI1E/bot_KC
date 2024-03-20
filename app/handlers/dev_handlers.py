from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from app.core.filter.is_admin import IsDeveloper

from app.core.keyboard import dev_keyboard, dev_change, back_to_menu_kb
from app.db.request import get_user, get_account
from app.utils.states import Change
from app.views.dev_views import dev_change_role

dev_router = Router()
dev_router.message.filter(IsDeveloper())
dev_router.callback_query.filter(IsDeveloper())


async def dev_start(message: types.Message):
    await message.answer("Здравствуй мой дорогой хозяин!\n"
                         "Отправляю вам вашу рабочую и тестовую клавиатуру!\n"
                         "Чем я могу тебе помочь?",
                         reply_markup=dev_keyboard()
                         )


@dev_router.callback_query(F.data == "Изменить статус пользователя")
async def start_change_status(call: types.CallbackQuery, state: FSMContext):
    await state.set_state(Change.surname)
    await call.message.edit_text("Введите фамилию сотрудника которому надо сменить статус:")


@dev_router.message(Change.surname)
async def confirm_change_status(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    data = await state.get_data()
    await state.clear()
    user = await get_user(surn=data["surname"], action="developer")
    if user:
        account = await get_account(user.id)
        await message.answer(f"Фамилия: {user.surname}\n"
                             f"Имя: {user.name}\n"
                             f"Отчество: {user.patronymic}\n"
                             f"Текущий статус: {account.status}\n\n"
                             f"На какой статус надо поменять?", reply_markup=dev_change(id_tg=account.id_tg))
    else:
        await message.answer("Что-то случилось!")


@dev_router.callback_query(F.data.startswith("chg"))
async def change_status(call: types.CallbackQuery) -> None:
    data = call.data.split("_")
    role = data[0]
    id_tg = int(data[1])
    await call.message.edit_text(await dev_change_role(id_tg=id_tg, role=role), reply_markup=back_to_menu_kb())
