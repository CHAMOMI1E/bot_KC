from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from app.core.filter.is_admin import IsAdmin
from app.core.sender import send_message

from app.db.request import get_accept_accounts
from app.core.keyboard import admin_keyboard, accept_text_kb, back_to_menu_kb
from app.utils.states import Post

admin_router = Router()
admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())


async def admin_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Ты авторизован(а) как админ",
                         reply_markup=admin_keyboard()
                         )


@admin_router.callback_query(F.data == "Отправить")
async def sender_news(call: types.CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text("Введите сообщение которое будет отправлено:", reply_markup=back_to_menu_kb())
    await state.set_state(Post.text)


@admin_router.message(Post.text)
async def accept_newsletter(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.set_state(None)
    await message.answer(f"Вы уверены что хотите отправить это сообщение?\n"
                         f"{data['text']}",
                         reply_markup=accept_text_kb())


@admin_router.callback_query(F.data == "text_accept")
async def accept_text_def(call: types.CallbackQuery, state: FSMContext):
    data1 = await state.get_data()
    print(data1)
    await state.clear()
    accounts = await get_accept_accounts()
    for account in accounts:
        print(account.id, account.id_tg, type(account.id_tg))
        if account.id_tg != call.from_user.id:
            await send_message(data1["text"], account.id_tg)
    await call.message.edit_text("Сообщение отправлено!")
    await call.message.answer("Хотите вернутся в главное меню?", reply_markup=back_to_menu_kb())
