from aiogram import types
from app.core.template_env import template_env


def check_admin(func):
    async def wrapper(message: types.Message, *args, **kwargs):
        if str(message.from_user.id) == "916134959":
            await func(message,  *args, **kwargs)
        else:
            await message.answer(template_env.get_template('error_message.html').render())
    return wrapper
