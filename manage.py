import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command

TOKEN = "5963841255:AAGfwJKvat72Vhq4uVUaZ9jyhsWJyOQ-sLE"
# Диспетчер
dp = Dispatcher()

menu = []


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id == 916134959:
        await message.answer("You are my father")
    else:
        await message.answer("hello")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
