from aiogram.filters import BaseFilter
from aiogram import types


class IsAdmin(BaseFilter):
    def __init__(self):
        pass

    def __call__(self, message: types.Message) -> bool:
        admin_id = 916134959
        return message.from_user.id == admin_id
