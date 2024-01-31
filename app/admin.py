from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from app.core.is_admin import IsAdmin
from app.core.sender import send_message

from app.db.request import get_users, get_accept_accounts, get_account, get_user_by_id_user, edit_user_id_db, \
    get_active_users
from app.core.keyboard import admin_keyboard, accept_text_kb, delete_accept
from app.utils.states import Post, Delete

admin_router = Router()
admin_router.message.filter(IsAdmin())


async def admin_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Ты авторизован(а) как админ",
                         reply_markup=admin_keyboard()
                         )


@admin_router.message(F.text.startswith("Просмотр"), IsAdmin())
async def admin_show_users(message: types.Message):
    users = await get_active_users()
    print("Callback query for showing users received.")
    text = "Список сотрудников: \n"
    for user in users:
        text = text + f"{user.id} {user.name} {user.surname}\n"
    await message.answer(f"{text}")


@admin_router.message(F.text.startswith("Отправить"), IsAdmin())
async def sender_news(message: types.Message, state: FSMContext):
    await message.answer("Введите сообщение которое будет отправлено:")
    await state.set_state(Post.text)


@admin_router.message(Post.text, IsAdmin())
async def accept_newsletter(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(f"Вы уверены что хотите отправить это сообщение?")
    await message.answer(f"{data['text']}",
                         reply_markup=accept_text_kb())


@admin_router.callback_query(F.data == "text_accept")
async def accept_text_def(call: types.CallbackQuery, state: FSMContext):
    # await message.edit_text()
    # await message.bot.send_message(message.from_user.id, message.text)
    await call.message.edit_text("Сообщение отправленно!")
    data1 = await state.get_data()
    print(data1)
    await state.clear()
    accounts = await get_accept_accounts()
    for account in accounts:
        print(account.id, account.id_tg, type(account.id_tg))
        await send_message(data1["text"], account.id_tg)


@admin_router.callback_query(F.data == "text_decline")
async def decline_text_def(message: types):
    print("Decline text")


# TODO сделать функцию и обработчик по измененнию статуса по фамилии
@admin_router.message(F.text == "Удалить", IsAdmin())
async def decline_user_by_surname(message: types.Message, state: FSMContext) -> None:
    await message.answer("Введите фамилию сотрудника который не будет получать рассылок")
    await state.set_state(Delete.surname)


@admin_router.message(Delete.surname, IsAdmin())
async def confirm_user_by_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    data = await state.get_data()
    user = await get_account(data["surname"])
    await state.clear()
    print(user.id)
    account = await get_user_by_id_user(user.id)
    await message.answer(f"Вы уверены что хотите удалить этого сотрудника? \n"
                         f"Фамилия: {user.surname}\n"
                         f"Имя: {user.name}\n"
                         f"Отчество: {user.patronymic}\n",
                         reply_markup=delete_accept(id_user=account.id_tg)
                         )


@admin_router.callback_query(F.data.startswith("delete_"), IsAdmin())
async def delete_callback_query(call: types.CallbackQuery) -> None:
    call_data = call.data.split("_")[1]
    await edit_user_id_db(int(call_data), False)
    await call.message.edit_text("Сотрудник удален")
    await send_message("Вы были заблокированы админом!", int(call_data))
    print(call_data)
