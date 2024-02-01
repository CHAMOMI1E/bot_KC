from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.core.decorators import kb_wrap


@kb_wrap(keyboard_type="inline", adjust_keyboard=2)
def accept_user_keyboard(
        builder: InlineKeyboardBuilder, user_id: int
) -> InlineKeyboardMarkup:
    action_types = ("accept", "decline")
    builder.button(text="ДА", callback_data=f"{action_types[0]}_{user_id}")
    builder.button(text="НЕТ", callback_data=f"{action_types[1]}_{user_id}")


@kb_wrap(keyboard_type="reply", adjust_keyboard=3)
def admin_keyboard(builder: ReplyKeyboardBuilder) -> ReplyKeyboardMarkup:
    builder.button(text="Отправить")
    builder.button(text="Удалить")
    builder.button(text="Просмотр")


@kb_wrap(keyboard_type="inline", adjust_keyboard=2)
def accept_text_kb(builder: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
    builder.button(text="yes".upper(), callback_data="text_accept")
    builder.button(text="no".upper(), callback_data="text_decline")


@kb_wrap(keyboard_type="inline", adjust_keyboard=2)
def delete_accept(builder: InlineKeyboardBuilder, id_user: int) -> InlineKeyboardMarkup:
    builder.button(text="yes".upper(), callback_data=f"delete_{id_user}")
    builder.button(text="no".upper(), callback_data=f"delete_decline")


@kb_wrap(keyboard_type="inline", adjust_keyboard=2)
def form_accept(builder: InlineKeyboardBuilder, name: str, surname: str, patronymic: str) -> InlineKeyboardMarkup:
    builder.button(text="верно".upper(), callback_data=f"forma_{name}_{surname}_{patronymic}")
    builder.button(text="переписать".upper(), callback_data=f"form_decline")
