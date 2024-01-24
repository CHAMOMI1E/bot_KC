import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.db.models import async_main
from config import TOKEN
from app.handlers import *
from app.views.form import register_router
# from app.views.accept_message import router_of_message


bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def main() -> None:
    await async_main()
    dp.include_routers(router,
                       register_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('stop')
