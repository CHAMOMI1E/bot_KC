from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from app.core.filter.is_admin import IsSuperAdmin
from app.core.sender import send_message

from app.db.request import get_user, edit_user_id_db, \
    get_active_users, get_decline_users, get_account
from app.core.keyboard import super_admin_keyboard, delete_accept, accept_unblock
from app.utils.states import Post, Delete, Unblock

sup_admin_router = Router()
sup_admin_router.message.filter(IsSuperAdmin())


async def super_admin_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Вы авторизованы как супер-админ",
                         reply_markup=super_admin_keyboard()
                         )


@sup_admin_router.message(F.data == "Просмотр")
async def admin_show_users(message: types.Message, state: FSMContext):
    await state.clear()
    users = await get_active_users()
    text = "Список сотрудников:\n"
    for user in users:
        text = text + f"👉 {user.surname} {user.name} {user.patronymic}\n"
    await message.answer(f"{text}")


@sup_admin_router.message(F.data == "Удалить")
async def decline_user_by_surname(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Введите фамилию сотрудника который не будет получать рассылок")
    await state.set_state(Delete.surname)


@sup_admin_router.message(F.data == "Разблокировать")
async def aclivate_declined_user(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    text = "Список заблокированных пользователей: \n"
    blocks = await get_decline_users()
    for block in blocks:
        text += f"👉 {block.surname} {block.name} {block.patronymic}\n"
    await message.answer(f"{text}" + "\nВведите фамилию пользователя которого хотите разблокировать:")
    await state.set_state(Unblock.surname)
    await message


@sup_admin_router.message(Unblock.surname)
async def unblock_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text.title())
    data = await state.get_data()
    await state.clear()
    user = await get_user(data["surname"], "undelete")
    if user:
        account = await get_account(user.id)
        await message.answer("Уверены что хотите отозвать права доступа у этого человека?\n \n"
                             f"Фамилия: {user.surname} \n"
                             f"Имя: {user.name} \n"
                             f"Отчество: {user.patronymic}",
                             reply_markup=accept_unblock(id_tg=account.id_tg))
    else:
        await message.answer(f"Сотрудник по фамилии {data['surname']} не найден!")


@sup_admin_router.callback_query(F.data == "text_decline")
async def decline_text_def(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите текст для сообщения:")
    await state.set_state(Post.text)


@sup_admin_router.message(Delete.surname)
async def confirm_user_by_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    data = await state.get_data()
    user = await get_user(data["surname"])
    if user:
        account = await get_account(user.id)
        await message.answer(f"Вы уверены что хотите отозвать права доступа у этого сотрудника? \n"
                             f"Фамилия: {user.surname}\n"
                             f"Имя: {user.name}\n"
                             f"Отчество: {user.patronymic}\n",
                             reply_markup=delete_accept(id_user=account.id_tg)
                             )
        await state.clear()
    else:
        await message.answer("Сотрудник не найден")


@sup_admin_router.callback_query(F.data.startswith("delete_"))
async def delete_callback_query(call: types.CallbackQuery) -> None:
    call_data = call.data.split("_")[1]
    await edit_user_id_db(int(call_data), False)
    await call.message.edit_text("У сотрудника были отозваны права доступа!")
    await send_message("У вас были отозваны права доступа администратором!", int(call_data), kb=ReplyKeyboardRemove())
    print(call_data)


@sup_admin_router.callback_query(F.data.startswith("unblock_"))
async def unblock_user(call: types.CallbackQuery) -> None:
    data = call.data.split("_")[1]
    await call.message.edit_text("Пользователю были выданы права доступа")
    await edit_user_id_db(int(data), True)
    await send_message("Вам выдали права доступа как сотрудника!", int(data))
