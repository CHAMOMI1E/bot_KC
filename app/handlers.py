from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(f"Hello, {message.from_user.full_name}!")