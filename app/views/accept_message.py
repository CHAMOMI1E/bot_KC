from aiogram import Router, F
from aiogram.types import Message

from manage import bot
from config import ADMIN
from app.core.template_env import template_env
from app.core.keyboard import accept_user_keyboard
from app.views.form import register_router

message_handler = Router()


# async def send_accept_message(name: str, surname: str, patronymic: str, chat_id: int):
#     template = template_env.get_template('accept_user.html').render(name=name, surname=surname, patronymic=patronymic,
#                                                                     id_tg=chat_id)
#     await bot.send_message(chat_id=ADMIN[0], text=template, reply_markup=accept_user_keyboard)


@register_router.callback_query(F.data == "accept_")
async def accept_message(message: Message):
    data = message.text.split("_")[1]
    data = int(data) if data.isdigit() else None
    print(data)
    await message.answer(f"{data}")
