import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command

from app.db.models import async_main
from config import TOKEN
from app.handlers import *
from app.views.form import register_router


# TOKEN = os.environ.get('TELEGRAM_API_TOKEN')



async def main() -> None:
    await async_main()
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_routers(router,
                      register_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('stop')
