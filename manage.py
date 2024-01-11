import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command

from app.handlers import router
from app.db.models import async_main
from config import TOKEN

menu = []


async def main() -> None:
    await async_main()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('stop')
