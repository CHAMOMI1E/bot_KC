from aiogram import F, Router, types

from app.db.request import accept_user_id_db

message_handler = Router()


@message_handler.callback_query(F.data.startswith("accept_"))
async def accept_message(call: types.CallbackQuery):
    data = call.data.split("_")[1]
    data = int(data) if data.isdigit() else None
    await accept_user_id_db(data, True)


@message_handler.callback_query(F.data.startswith("decline_"))
async def accept_message(call: types.CallbackQuery):
    data = call.data.split("_")[1]
    data = int(data) if data.isdigit() else None
    await accept_user_id_db(data, False)
