from aiogram.filters import BaseFilter
from aiogram import types


class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        admin_id = 916134959
        return message.from_user.id == admin_id
