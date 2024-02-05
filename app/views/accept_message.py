from aiogram import F, Router, types

from app.core.sender import send_message
from app.db.request import edit_user_id_db

message_handler = Router()


@message_handler.callback_query(F.data.startswith("accept_"))
async def accept_message(call: types.CallbackQuery):
    data = call.data.split("_")[1]
    surname = call.data.split("_")[2]
    await call.message.edit_text(f"Человек по фамилии {surname} был добавлен в базу")
    data = int(data) if data.isdigit() else None
    await edit_user_id_db(data, True)
    await send_message("Вы были подтверждены админом!", int(data))


@message_handler.callback_query(F.data.startswith("decline_"))
async def accept_message(call: types.CallbackQuery):
    data = call.data.split("_")[1]
    surname = call.data.split("_")[2]
    await call.message.edit_text(f"Человеку по фамилии {surname} было отказано в правах доступа")
    data = int(data) if data.isdigit() else None
    await edit_user_id_db(data, False)
    await send_message("Вам было отказано в правах доступа", int(data))
