from typing import Tuple, Dict

from sqlalchemy.orm import make_transient

from app.db.models import Users, Accounts, async_session, Status
from sqlalchemy import select
from sqlalchemy import update


async def get_users() -> Dict:
    async with async_session() as session:
        result = await session.execute(select(Users))
        return result.scalars().all()


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


async def edit_user_id_db(id_teleg: int, status: bool) -> None:
    async with async_session() as session:
        try:
            # поиск аккаунта с нужным id в базе
            statement = select(Accounts).where(Accounts.id_tg == id_teleg)
            result = await session.execute(statement)
            account = result.scalar()
            if account:
                # изменение статуса в зависимости от того какой статус был выдан
                if status:
                    account.status = Status.ACTIVE.value
                    await session.commit()
                    print(f"Пользователь с ID {id_teleg} был подключен и подтвержден админом")
                else:
                    account.status = Status.DISABLE.value
                    await session.commit()
                    print(f"Пользователь с ID {id_teleg} был отключен админом")
        # ловля ошибок по бд)
        except Exception as e:
            print("Error adding user info:", e)
            await session.rollback()


async def get_user_by_id(id_teleg: int):
    async with async_session() as session:
        result = await session.execute(select(Accounts).filter_by(id_tg=id_teleg))
        existing_user = result.scalars().first()
        return existing_user
