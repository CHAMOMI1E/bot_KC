from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from app.core.is_admin import IsAdmin
from app.core.sender import send_message

from app.db.request import get_accept_accounts, get_account, get_user_by_id_user, edit_user_id_db, \
    get_active_users, get_decline_accounts
from app.core.keyboard import admin_keyboard, accept_text_kb, delete_accept
from app.utils.states import Post, Delete, Unblock

admin_router = Router()
admin_router.message.filter(IsAdmin())


async def admin_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Ты авторизован(а) как админ",
                         reply_markup=admin_keyboard()
                         )


@admin_router.message(F.text.startswith("Просмотр"), IsAdmin())
async def admin_show_users(message: types.Message, state: FSMContext):
    await state.clear()
    users = await get_active_users()
    text = "Список сотрудников:\n"
    for user in users:
        text = text + f"👉 {user.surname} {user.name} {user.patronymic}\n"
    await message.answer(f"{text}")


@admin_router.message(F.text.startswith("Отправить"), IsAdmin())
async def sender_news(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Введите сообщение которое будет отправлено:")
    await state.set_state(Post.text)


@admin_router.message(F.text.startswith("Удалить"), IsAdmin())
async def decline_user_by_surname(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Введите фамилию сотрудника который не будет получать рассылок")
    await state.set_state(Delete.surname)


@admin_router.message(F.text.startswith("Разблокировать"), IsAdmin())
async def aclivate_declined_user(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    text = "Список заблокированных пользователей: \n"
    blocks = await get_decline_accounts()
    for block in blocks:
        text += f"👉 {block.surname} {block.name} {block.patronymic}\n"
    await message.answer(f"{text}" + "\nВведите фамилию пользователя которого хотите разблокировать:")
    await state.set_state(Unblock.surname)


@admin_router.message(Unblock.surname, IsAdmin)
async def unblock_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    data = await state.get_data()
    data = get_blocked_user



@admin_router.message(Post.text, IsAdmin())
async def accept_newsletter(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(f"Вы уверены что хотите отправить это сообщение?")
    await message.answer(f"{data['text']}",
                         reply_markup=accept_text_kb())


@admin_router.callback_query(F.data == "text_accept")
async def accept_text_def(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Сообщение отправленно!")
    data1 = await state.get_data()
    print(data1)
    await state.clear()
    accounts = await get_accept_accounts()
    for account in accounts:
        print(account.id, account.id_tg, type(account.id_tg))
        await send_message(data1["text"], account.id_tg)
    await call.message.edit_text("Сообщение отправлено")


@admin_router.callback_query(F.data == "text_decline")
async def decline_text_def(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите текст для сообщения:")
    await state.set_state(Post.text)


@admin_router.message(Delete.surname, IsAdmin())
async def confirm_user_by_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    data = await state.get_data()
    try:
        user = await get_account(data["surname"])
        await state.clear()
        account = await get_user_by_id_user(user.id)
        await message.answer(f"Вы уверены что хотите удалить этого сотрудника? \n"
                             f"Фамилия: {user.surname}\n"
                             f"Имя: {user.name}\n"
                             f"Отчество: {user.patronymic}\n",
                             reply_markup=delete_accept(id_user=account.id_tg)
                             )
    except Exception:
        await message.answer("Сотрудник не найден")


@admin_router.callback_query(F.data.startswith("delete_"), IsAdmin())
async def delete_callback_query(call: types.CallbackQuery) -> None:
    call_data = call.data.split("_")[1]
    await edit_user_id_db(int(call_data), False)
    await call.message.edit_text("Сотрудник удален")
    await send_message("Вы были заблокированы админом!", int(call_data))
    print(call_data)
