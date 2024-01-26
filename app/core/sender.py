from aiogram import Bot

from app.core.keyboard import accept_user_keyboard
from app.core.template_env import template_env
from config import ADMIN, TOKEN


async def send_accept_message(name: str, surname: str, patronymic: str, chat_id: int):
    template = template_env.get_template("accept_user.html").render(
        name=name,
        surname=surname,
        patronymic=patronymic,
        id_tg=chat_id
    )

    bot_sender = Bot(TOKEN)
    try:
        await bot_sender.send_message(
            chat_id=ADMIN[0],
            text=template,
            reply_markup=accept_user_keyboard(user_id=chat_id)
        )
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        await bot_sender.session.close()