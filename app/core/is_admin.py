from config import DEVELOPER_ID

from aiogram.filters import BaseFilter
from aiogram import types
from app.db.request import search_admin


class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        account = await search_admin(message.from_user.id)
         
