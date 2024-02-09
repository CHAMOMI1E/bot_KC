from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from app.db.models import Status
from app.db.request import get_user_by_id_tg, get_account
from app.handlers.admin import admin_start
from app.handlers.dev_handlers import dev_start
from app.handlers.super_admin import super_admin_start
from app.utils.states import Form
from app.views.main_view import get_main_kb

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    user = await get_user_by_id_tg(message.from_user.id)
    if user:
        if user.status == Status.ACTIVE.value:
            await message.answer(f"Вы уже зарегистрированы!")
        elif user.status == Status.DISABLE.value:
            await message.answer(f"У вас нет прав доступа")
        elif user.status == Status.UNKNOWN.value:
            await message.answer(f"Ожидайте подтверждения администратора...")
        elif user.status == Status.SUPER_ADMIN.value:
            await super_admin_start(message)
        elif user.status == Status.ADMIN.value:
            await admin_start(message)
        elif user.status == Status.DEVELOPER.value:
            await dev_start(message)
    else:
        await state.set_state(Form.surname)
        await message.answer("Привет. Для начала введите свою фаимилию:")


@router.callback_query(F.data == "cancel")
async def cancel(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text("Операция отменена")


@router.callback_query(F.data == "menu")
async def menu(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    account = await get_account(call.from_user.id, "dev")
    kb = await get_main_kb(account.id_tg)
    await call.message.edit_text("Ваше меню", reply_markup=kb)