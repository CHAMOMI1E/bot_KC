import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from app.db.models import async_main
from app.handlers.super_admin import sup_admin_router
from config import TOKEN_TEST
from app.handlers.admin import admin_router
from app.handlers.handlers import router
from app.views.form import register_router
from app.views.accept_message import message_handler
from app.handlers.dev_handlers import dev_router

bot = Bot(TOKEN_TEST, parse_mode=ParseMode.HTML)
dp = Dispatcher()


async def main() -> None:
    await async_main()
    dp.include_routers(router,
                       register_router,
                       message_handler,
                       admin_router,
                       sup_admin_router,
                       dev_router,
                       )

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('stop')





