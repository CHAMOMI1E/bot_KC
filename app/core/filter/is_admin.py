from aiogram.filters import BaseFilter
from aiogram import types
from app.core.filter.filter_request import search_admin, search_super_admin, search_developer


class IsAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        account = await search_admin(message.from_user.id)
        if account:
            return True
        else:
            return False


class IsSuperAdmin(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        account = await search_super_admin(message.from_user.id)
        if account:
            return True
        else:
            return False


class IsDeveloper(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        account = await search_developer(message.from_user.id)
        if account:
            return True
        else:
            return False
