from aiogram import types


def check_admin(func):
    async def wrapper(message: types.Message, *args, **kwargs):
        if str(message.from_user.id) == "9161349591":
            await func(message,  *args, **kwargs)
        else:
            await message.answer("Ты не админ")
    return wrapper
