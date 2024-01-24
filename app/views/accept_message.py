from aiogram import Router, F, types

from config import ADMIN
from app.core.template_env import template_env
from app.core.keyboard import accept_user_keyboard


message_handler = Router()


@message_handler.callback_query(F.data == "accept_")
async def accept_message(message: types.Message):
    data = message.text.split("_")[1]
    data = int(data) if data.isdigit() else None
    print(data)
    await message.answer(f"{data}")


