from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton

from app.db.request import get_users

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить', callback_data='send_text')],
                                     [KeyboardButton(text='Удалить', callback_data='delete_user')],
                                     [KeyboardButton(text='Просмотр', callback_data='show_users')]
                                     ])


async def main_keyboard():
    users_kb = InlineKeyboardBuilder()
    users = await get_users()
    for user in users:
        users_kb.add(InlineKeyboardButton(text=user.tg_id, callback_data=f'{user.id}'))
    return users_kb.adjust(2).as_markup()