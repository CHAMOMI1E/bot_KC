from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from app.core.is_admin import IsAdmin

from app.db.request import get_users
from app.core.keyboard import admin_keyboard, accept_text
from app.utils.states import Post

admin_router = Router()
admin_router.message.filter(IsAdmin())


async def admin_start(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}! "
                         f"Ты авторизован(а) как админ",
                         reply_markup=admin_keyboard()
                         )


@admin_router.callback_query(F.data.startswith("show_users"))
async def admin_show_users(message: types.Message):
    users = get_users()
    text = "Список сотрудников: \n"
    for user in users:
        text = text + f"{user.id} {user.name}\n"


@admin_router.callback_query(F.data.startswith("send_text"))
async def sender_news(message: types.Message, state: FSMContext):
    await state.set_state(Post.text)
    await message.answer("Введите сообщение которое будет отправлено:")


@admin_router.message(Post.text)
async def accept_newsletter(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await message.answer(f"Вы уверены что хотите отправить это сообщение? \n"
                         f"{data['text']}",
                         reply_markup=accept_text())


@admin_router.callback_query(Post.text, F.data.startswith("accept_text"))
async def accept_text(message: types.Message, state: FSMContext):
    await message.answer("Текст отправлен")
    data = await state.get_data()
    await state.clear()
    # TODO сделать функцию для отправки сообщения всем подтвежденным пользователям и request функцию для получения
    #  ids пользователей с подтвержденными статусами


@admin_router.message(F.text == "test")
async def test(message: types.Message) -> None:
    await message.answer("Test admin")


@admin_router.error
