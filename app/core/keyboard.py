from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from app.core.decorators import kb_wrap


@kb_wrap(keyboard_type="inline", adjust_keyboard=2)
def accept_user_keyboard(
        builder: InlineKeyboardBuilder,
        user_id: int,
        surname: str
) -> InlineKeyboardMarkup:
    action_types = ("accept", "decline")
    builder.button(text="ДА", callback_data=f"{action_types[0]}_{user_id}_{surname}")
    builder.button(text="НЕТ", callback_data=f"{action_types[1]}_{user_id}_{surname}")


@kb_wrap(keyboard_type="reply", adjust_keyboard=1)
def admin_keyboard(builder: ReplyKeyboardBuilder) -> ReplyKeyboardMarkup:
    builder.button(text="Отправить".title())


@kb_wrap(keyboard_type="inline", adjust_keyboard=2)
def accept_text_kb(builder: InlineKeyboardBuilder) -> InlineKeyboardMarkup:
    builder.button(text="верно".upper(), callback_data="text_accept")
    builder.button(text="неверно".upper(), callback_data="cancel")


@kb_wrap(keyboard_type="inline", adjust_keyboard=2)
def delete_accept(builder: InlineKeyboardBuilder, id_user: int) -> InlineKeyboardMarkup:
    builder.button(text="да".upper(), callback_data=f"delete_{id_user}")
    builder.button(text="нет".upper(), callback_data=f"cancel")


@kb_wrap(keyboard_type="inline", adjust_keyboard=2)
def form_accept(builder: InlineKeyboardBuilder, name: str, surname: str, patronymic: str) -> InlineKeyboardMarkup:
    builder.button(text="верно".upper(), callback_data=f"forma_{name}_{surname}_{patronymic}")
    builder.button(text="переписать".upper(), callback_data=f"form_decline")


@kb_wrap(keyboard_type="inline", adjust_keyboard=2)
def accept_unblock(builder: InlineKeyboardBuilder, id_tg: int) -> InlineKeyboardMarkup:
    builder.button(text="да".upper(), callback_data=f"unblock_{id_tg}")
    builder.button(text="нет".upper(), callback_data="cancel")


@kb_wrap(keyboard_type="reply", adjust_keyboard=(3, 1))
def super_admin_keyboard(builder: ReplyKeyboardBuilder) -> ReplyKeyboardMarkup:
    builder.button(text="Отправить".title())
    builder.button(text="Удалить".title())
    builder.button(text="Просмотр".title())
    builder.button(text="Разблокировать".title())


@kb_wrap(keyboard_type="reply", adjust_keyboard=(3, 1, 1))
def dev_keyboard(builder: ReplyKeyboardBuilder) -> ReplyKeyboardMarkup:
    builder.button(text="Отправить".title())
    builder.button(text="Удалить".title())
    builder.button(text="Просмотр".title())
    builder.button(text="Изменить статус пользователя")
    builder.button(text="Статистика".title())


delete_rkb = ReplyKeyboardRemove()


@kb_wrap(keyboard_type="inline", adjust_keyboard=(3, 1))
def dev_change(builder: InlineKeyboardBuilder, id_tg: int) -> InlineKeyboardMarkup:
    builder.button(text="active".upper(), callback_data=f"chg-active_{id_tg}")
    builder.button(text="disable".upper(), callback_data=f"chg-disable_{id_tg}")
    builder.button(text="admin".upper(), callback_data=f"chg-admin_{id_tg}")
    builder.button(text="super admin".upper(), callback_data=f"chg-superadmin_{id_tg}")
