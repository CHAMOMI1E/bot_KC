from aiogram.types import InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, ReplyKeyboardBuilder

from app.core.decorators import kb_wrap
from app.db.request import get_users

accept = [
    [InlineKeyboardButton(text="Accept", callback_data="accept_register")],
    [InlineKeyboardButton(text="Decline", callback_data="decline_register")],
]
accept_keyboard = InlineKeyboardMarkup(inline_keyboard=accept, resize_keyboard=True)


@kb_wrap(keyboard_type="inline", adjust_keyboard=2)
def accept_user_keyboard(
        builder: InlineKeyboardBuilder, user_id: int
) -> InlineKeyboardMarkup:
    action_types = ("accept", "decline")
    builder.button(text="ДА", callback_data=f"{action_types[0]}_{user_id}")
    builder.button(text="НЕТ", callback_data=f"{action_types[1]}_{user_id}")


async def main_keyboard():
    users_kb = InlineKeyboardBuilder()
    users = await get_users()
    for user in users:
        users_kb.add(InlineKeyboardButton(text=user.tg_id, callback_data=f"{user.id}"))
    return users_kb.adjust(2).as_markup()


@kb_wrap(keyboard_type="reply", adjust_keyboard=3)
def admin_keyboard(builder: ReplyKeyboardBuilder) -> ReplyKeyboardMarkup:
    builder.button(text="Отправить", callback_data="send_text")
    builder.button(text="Удалить", callback_data="delete_user")
    builder.button(text="Просмотр", callback_data="show_users")


@kb_wrap(keyboard_type="inline", adjust_keyboard=2)
def accept_text(builder: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
    builder.button(text="yes".upper(), callback_data="accept_text")
    builder.button(text="no".upper(), callback_data="decline_text")
