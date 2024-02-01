from aiogram.types import Message
from aiogram.filters import CommandStart

from config import ADMIN

from app.views.main_view import *
from app.admin import *

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN:
        await admin_start(message)
    else:
        await check_user_in_db(message, state)
