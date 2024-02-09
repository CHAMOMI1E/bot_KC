from app.core.keyboard import admin_keyboard, super_admin_keyboard
from app.core.sender import send_message
from app.db.models import Status
from app.db.request import get_account, dev_update_status
from aiogram.types import ReplyKeyboardRemove


async def dev_change_role(id_tg: int, role: str) -> None:
    account = await get_account(id_tg=id_tg, action="dev")
    if account:
        if role == "chg-active":
            await send_message("Вам выдали права доступа пользователя!", chat_id=id_tg, kb=ReplyKeyboardRemove())
            return await dev_update_status(id_tg, f"{Status.ACTIVE.value}")
        elif role == "chg-disable":
            await send_message("У вас были отозваны права доступа!", chat_id=id_tg, kb=ReplyKeyboardRemove())
            return await dev_update_status(id_tg, f"{Status.DISABLE.value}")
        elif role == "chg-admin":
            await send_message("Вам выдали права доступа администратора!", chat_id=id_tg, kb=admin_keyboard())
            return await dev_update_status(id_tg, f"{Status.ADMIN.value}")
        elif role == "chg-superadmin":
            await send_message("Вам выдали права доступа супер-администратора!", chat_id=id_tg, kb=super_admin_keyboard())
            return await dev_update_status(id_tg, f"{Status.SUPER_ADMIN.value}")
        else:
            return "Something went wrong 1"
    else:
        return "Something went wrong 2"

