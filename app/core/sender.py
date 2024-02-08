from typing import Optional, Union

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

from config import TOKEN_TEST
from aiogram import Bot

from app.core.keyboard import accept_user_keyboard
from app.core.template_env import template_env
from app.db.request import get_super_admin


# TODO ПЕРЕДЕЛАТЬ РАССЫЛКУ АДМИНА НА СУПЕР_АДМИАН
async def send_accept_message(name: str, surname: str, patronymic: str, chat_id: int):
    template = template_env.get_template("accept_user.html").render(
        name=name,
        surname=surname,
        patronymic=patronymic,
    )

    bot_sender = Bot(TOKEN_TEST)
    try:
        sa = await get_super_admin()
        await bot_sender.send_message(
            chat_id=sa.id_tg,
            text=template,
            reply_markup=accept_user_keyboard(user_id=chat_id, surname=surname)
        )
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        await bot_sender.session.close()


async def send_message(text: str, chat_id: int, kb: Optional[
            Union[InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove]
        ] = None) -> None:
    bot_sender = Bot(TOKEN_TEST)
    try:
        await bot_sender.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=kb,
        )
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        await bot_sender.session.close()
