from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton

from app.db.request import get_user

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить')],
                                     [KeyboardButton(text='Удалить')],
                                     [KeyboardButton(text='Просмотр')]
                                     ])


async def main_keyboard():
    users_kb = InlineKeyboardBuilder()
    users = await get_user()
    for user in users:
        users_kb.add(InlineKeyboardButton(text=user.tg_id, callback_data=f'{user.id}'))
    return users_kb.adjust(2).as_markup()