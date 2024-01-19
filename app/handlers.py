from aiogram.types import Message
from aiogram.filters import CommandStart

from config import ADMIN

from app.views.main_view import *
from app.views.form import *
from app.admin import *

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    # await message.answer(await check_user_in_db(message))
    if message.from_user.id in ADMIN:
        await admin_start(message)
    else:
        await check_user_in_db(message)


# @dp.message_handler(callback_query=lambda message: True)
# async def list_users(message: Message):
#     await message.answer("Список юзеров", reply_markup=await kb.main_keyboard())
