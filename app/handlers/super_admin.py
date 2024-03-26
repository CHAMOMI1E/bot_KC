from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from app.core.filter.is_admin import IsSuperAdmin
from app.core.sender import send_message
from app.db.models import Status

from app.db.request import edit_user_id_db, \
    get_active_users, get_decline_users, get_account, dev_update_status, get_user_for_ta_admin, get_user_for_undelete, \
    get_user_for_delete
from app.core.keyboard import super_admin_keyboard, delete_accept, accept_unblock, back_to_menu_kb, accept_admin_kb, \
    admin_keyboard, take_away_admin_kb
from app.utils.states import Post, Delete, Unblock, NewAdmin, TakeAwayAdmin

sup_admin_router = Router()
sup_admin_router.message.filter(IsSuperAdmin())
# sup_admin_router.callback_query.filter(IsSuperAdmin())


async def super_admin_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Вы авторизованы как супер-админ",
                         reply_markup=super_admin_keyboard()
                         )


@sup_admin_router.callback_query(F.data == "Просмотр")
async def admin_show_users(call: types.CallbackQuery, state: FSMContext):
    await state.clear()
    admins, users = await get_active_users()
    list_of_users: str = ""
    list_of_admins: str = ""
    for admin in admins:
        list_of_admins = list_of_admins + f"👉 {admin.surname} {admin.name} {admin.patronymic}\n"
    for user in users:
        list_of_users = list_of_users + f"👉 {user.surname} {user.name} {user.patronymic}\n"
    await call.message.edit_text(f"Список админов:\n"
                                 f"{list_of_admins}\n\n"
                                 f"Список сотрудников:\n"
                                 f"{list_of_users}")
    await call.message.answer("Хотите вернутся в главное меню?", reply_markup=back_to_menu_kb())


@sup_admin_router.callback_query(F.data == "Заблокировать")
async def decline_user_by_surname(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text("Введите фамилию сотрудника который не будет получать рассылок",
                                 reply_markup=back_to_menu_kb())
    await state.set_state(Delete.surname)


@sup_admin_router.callback_query(F.data == "Разблокировать")
async def aclivate_declined_user(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    text = "Список заблокированных пользователей: \n"
    blocks = await get_decline_users()
    for block in blocks:
        text += f"👉 {block.surname} {block.name} {block.patronymic}\n"
    await call.message.edit_text(f"{text}" + "\nВведите фамилию пользователя которого хотите разблокировать:",
                                 reply_markup=back_to_menu_kb())
    await state.set_state(Unblock.surname)


@sup_admin_router.callback_query(F.data == "Сделать админом")
async def add_admin(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text("Введите фамилию сотрудника которому надо выдать права администратора",
                                 reply_markup=back_to_menu_kb())
    await state.set_state(NewAdmin.surname)


@sup_admin_router.callback_query(F.data == "Отобрать права админа")
async def take_away_admin(call: types.CallbackQuery, state: FSMContext) -> TakeAwayAdmin.surname:
    await state.clear()
    await call.message.edit_text("Введите фамилию сотрудника у которого хотите отобрать права админа",
                                 reply_markup=back_to_menu_kb())
    await state.set_state(TakeAwayAdmin.surname)


@sup_admin_router.callback_query(F.data == "text_decline")
async def decline_text_def(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Введите текст для сообщения:")
    await state.set_state(Post.text)


@sup_admin_router.callback_query(F.data.startswith("delete_"))
async def delete_callback_query(call: types.CallbackQuery) -> None:
    call_data = call.data.split("_")[1]
    await edit_user_id_db(int(call_data), False)
    await call.message.edit_text("У сотрудника были отозваны права доступа!")
    await send_message("У вас были отозваны права доступа администратором!", int(call_data))
    await call.message.answer("Хотите вернутся в главное меню?", reply_markup=back_to_menu_kb())


@sup_admin_router.callback_query(F.data.startswith("unblock_"))
async def unblock_user(call: types.CallbackQuery) -> None:
    data = call.data.split("_")[1]
    await call.message.edit_text("Пользователю были выданы права доступа", reply_markup=back_to_menu_kb())
    await edit_user_id_db(int(data), True)
    await send_message("Вам выдали права доступа как сотрудника!", int(data))


@sup_admin_router.callback_query(F.data.startswith("admin-accept"))
async def finish_add_admin_message(call: types.CallbackQuery) -> None:
    data = call.data.split("_")[1]
    await call.message.edit_text(await dev_update_status(int(data), Status.ADMIN.value), reply_markup=back_to_menu_kb())
    await send_message("Вам выдали права администратора", int(data), admin_keyboard())


@sup_admin_router.callback_query(F.data.startswith("take-away-admin_"))
async def take_admin(call: types.CallbackQuery) -> None:
    data = call.data.split("_")[1]
    await call.message.edit_text(await dev_update_status(int(data), Status.ACTIVE.value),
                                 reply_markup=back_to_menu_kb())
    await send_message("У вас были отозваны права администратора", int(data), None)


@sup_admin_router.message(TakeAwayAdmin.surname)
async def remove_admin(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text.title())
    data = await state.get_data()
    await state.set_state(None)
    print(data)
    user = await get_user_for_ta_admin(data["surname"])
    if user:
        account = await get_account(user.id)
        await message.answer("Вы уверены что хотите отобрать права администратора у этого чловека?\n"
                             f"Фамилия: {user.surname}\n"
                             f"Имя: {user.name}\n"
                             f"Отчество: {user.patronymic}\n",
                             reply_markup=take_away_admin_kb(id_tg=account.id_tg))
    else:
        await message.answer("Администратор с такой фамилией не найден!", reply_markup=back_to_menu_kb())


@sup_admin_router.message(Unblock.surname)
async def unblock_user(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text.title())
    data = await state.get_data()
    await state.clear()
    user = await get_user_for_undelete(data["surname"])
    if user:
        account = await get_account(user.id)
        await message.answer("Уверены что хотите вернуть права доступа этому человеку?\n \n"
                             f"Фамилия: {user.surname} \n"
                             f"Имя: {user.name} \n"
                             f"Отчество: {user.patronymic}",
                             reply_markup=accept_unblock(id_tg=account.id_tg))

    else:
        await message.answer(f"Сотрудник по фамилии {data['surname']} не найден!", reply_markup=back_to_menu_kb())


@sup_admin_router.message(Delete.surname)
async def confirm_user_by_surname(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    data = await state.get_data()
    user = await get_user_for_delete(data["surname"])
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
        await message.answer("Сотрудник не найден", reply_markup=back_to_menu_kb())


@sup_admin_router.message(NewAdmin.surname)
async def add_admin_message(message: types.Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text.title())
    data = await state.get_data()
    await state.clear()
    user = await get_user_for_delete(data["surname"])
    if user:
        account = await get_account(user.id)
        if account.status not in [Status.ADMIN.value, Status.SUPER_ADMIN.value, Status.DEVELOPER.value,
                                  Status.DISABLE.value]:
            await message.answer(f"Вы уверены что хотите выдать этому сотруднику права доступа админа?\n"
                                 f"Фамилия: {user.surname}\n"
                                 f"Имя: {user.name}\n"
                                 f"Отчество: {user.patronymic}\n",
                                 reply_markup=accept_admin_kb(id_tg=account.id_tg))
        else:
            await message.answer("У этого человека статус равный вам или выше, обращайтесь к разработчику!",
                                 reply_markup=back_to_menu_kb())
