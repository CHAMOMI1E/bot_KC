from aiogram.types import Message
from aiogram.filters import CommandStart

from config import DEVELOPER_ID

from app.views.main_view import *
from app.admin import *

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = await get_user_by_id_tg(message.from_user.id)
    if user:
        if user.status == Status.ACTIVE.value:
            await message.answer(f"Вы уже зарегистрированы!")
        elif user.status == Status.DISABLE.value:
            await message.answer(f"У вас нет прав доступа")
        elif user.status == Status.UNKNOWN.value:
            await message.answer(f"Ожидайте подтверждения администратора...")
        elif user.status == Status.SUPER_ADMIN.value:
            print("Проверку прошёл")
            await admin_start(message)
        elif user.status == Status.ADMIN.value:
            await admin_start(message)
        # elif message.from_user.id == DEVELOPER_ID:
        #     await admin_start(message)
    else:
        await state.set_state(Form.surname)
        await message.answer("Привет. Для начала введите свою фаимилию:")
