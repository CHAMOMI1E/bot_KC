from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder, InlineKeyboardButton

from app.db.request import get_users

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отправить', callback_data='send_text')],
                                     [KeyboardButton(text='Удалить', callback_data='delete_user')],
                                     [KeyboardButton(text='Просмотр', callback_data='show_users')]
                                     ])

accept = [
    [InlineKeyboardButton(text="Accept", callback_data="accept_register")],
    [InlineKeyboardButton(text="Decline", callback_data="decline_register")]
]
accept_keyboard = InlineKeyboardMarkup(inline_keyboard=accept, resize_keyboard=True)


async def main_keyboard():
    users_kb = InlineKeyboardBuilder()
    users = await get_users()
    for user in users:
        users_kb.add(InlineKeyboardButton(text=user.tg_id, callback_data=f'{user.id}'))
    return users_kb.adjust(2).as_markup()


# TODO сделать инлайн клаву для подтверждения личности
async def accept_register():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Yes', callback_data='accept'),
        InlineKeyboardButton(text='No', callback_data='decline'))
