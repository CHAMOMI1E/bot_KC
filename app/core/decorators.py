from aiogram import types
from config import ADMIN
from app.core.template_env import template_env


def check_admin(func):
    async def wrapper(message: types.Message, *args, **kwargs):
        if message.from_user.id in ADMIN:
            await func(message,  *args, **kwargs)
        else:
            await message.answer(template_env.get_template('error_message.html').render())
    return wrapper
