from aiogram import F, Router, types

message_handler = Router()


data = "accept_128131271723"


@message_handler.callback_query(F.data.startswith("accept_"))
async def accept_message(call: types.CallbackQuery):
    data = call.data.split("_")[1]
    data = int(data) if data.isdigit() else None
    print(data)
    await call.message.answer(f"{data}")
