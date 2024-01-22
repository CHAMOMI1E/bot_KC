from app.db.models import Users, Accounts, async_session, Status
from sqlalchemy import select


async def get_users():
    async with async_session() as session:
        result = await session.execute(select(Users))
        return result.scalars().all()


# async def add_user(name: str, surname: str, patronymic: str, id_tg: int) -> None:
#     async with async_session() as session:
#         try:
#             # создание экземпляра пользователя
#             new_user = Users(name=name, surname=surname, patronymic=patronymic)
#             session.add(new_user)
#             await session.flush()  # чтобы получить id пользователя
#
#             # создание экземпляра аккаунта
#             new_account = Accounts(id_tg=id_tg, status=Status.UNKNOWN, id_user=new_user.id)
#             await session.add(new_account)
#
#             session.commit()  # сохранение изменений в базе данных
#             print(f'Пользователь под id {new_account.id_user} был добавлен в базу!')
#
#         except Exception as e:
#             print("Error adding user info:", e)
#             await session.rollback()
#         # return
async def add_user(name: str, surname: str, patronymic: str, id_tg: int) -> None:
    async with async_session() as session:
        try:
            # создание экземпляра пользователя
            new_user = Users(name=name, surname=surname, patronymic=patronymic)
            session.add(new_user)
            await session.flush()  # чтобы получить id пользователя

            # создание экземпляра аккаунта
            new_account = Accounts(id_tg=id_tg, status=Status.UNKNOWN.value, id_user=new_user.id)
            session.add(new_account)

            await session.commit()  # дождаться выполнения операции, чтобы сохранить изменения в базе данных
            print(f'Пользователь под id {new_account.id_user} был добавлен в базу!')

        except Exception as e:
            print("Error adding user info:", e)
            await session.rollback()


async def get_user_by_id(id_teleg: int):
    async with async_session() as session:
        result = await session.execute(select(Accounts).filter_by(id_tg=id_teleg))
        existing_user = result.scalars().first()
        return existing_user
