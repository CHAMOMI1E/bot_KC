from typing import Dict, Literal

from app.db.models import Users, Accounts, async_session, Status
from sqlalchemy import select


# TODO ПЕРЕДЕЛАТЬ ВСЕ ЗАПРОСЫ И СДЕЛАТЬ КОД БОЛЕЕ КОМПАКНТЫМ!!!
async def get_active_users() -> Dict:
    async with async_session() as session:
        # Запрос, чтобы получить всех пользователей со статусом ACTIVE
        result = await session.execute(
            select(Users).join(Accounts).where(Accounts.status == Status.ACTIVE.value)
        )
        # Возвращаем результат запроса
        return result.scalars().all()


async def get_decline_users():
    async with async_session() as session:
        blocks = await session.execute(
            select(Users).join(Accounts).where(Accounts.status == Status.DISABLE.value)
        )
        return blocks.scalars().all()


async def get_blocked_user(surname: str) -> Dict:
    async with async_session() as session:
        user = await session.execute(
            select(Users).join(Accounts, Accounts).where(Accounts.status == Status.DISABLE.value,
                                                         Users.surname == surname)
        )
        return user.scalars().first()


async def get_disable_user_by_surname(surname: str) -> Users:
    async with async_session() as session:
        try:
            account = await session.execute(
                select(Accounts)
                .join(Users)
                .where(Accounts.status == Status.DISABLE.value, Users.surname == surname)
            )
            return account.scalars().first()
        except Exception as e:
            print(e)
            return None


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


async def get_user_by_id_tg(id_teleg: int) -> Accounts:
    async with async_session() as session:
        result = await session.execute(select(Accounts).filter_by(id_tg=id_teleg))
        existing_user = result.scalars().first()
        return existing_user


async def get_account_by_id_user(id_user: int) -> Accounts:
    async with async_session() as session:
        try:
            result = await session.execute(select(Accounts).filter_by(id_user=id_user))
            existing_user = result.scalars().first()
            return existing_user
        except Exception as e:
            print(e)
            return False


async def get_accept_accounts():
    async with async_session() as session:
        async with session.begin():
            stmt = select(Accounts).where(
                Accounts.status
                .in_(
                    [Status.ADMIN.value, Status.SUPER_ADMIN.value, Status.DEVELOPER.value, Status.ACTIVE.value]
                ))
            result = await session.execute(stmt)
            accounts_with_desired_status = result.scalars().all()
    return accounts_with_desired_status


async def get_user(surn: str, action: Literal["delete", "undelete", None] = "delete") -> Accounts | None:
    async with async_session() as session:
        try:
            if action == "delete":
                user = await session.execute(
                    select(Users)
                    .join(Accounts)
                    .where(Accounts.status == Status.ACTIVE.value,
                           Users.surname == surn)
                )
                return user.scalars().first()
            elif action == "undelete":
                user = await session.execute(
                    select(Users)
                    .join(Accounts)
                    .where(Accounts.status == Status.DISABLE.value,
                           Users.surname == surn)
                )
                return user.scalars().first()
            else:
                user = await session.execute(
                    select(Users)
                    .where(Users.surname == surn)
                )
                return user.scalars().first()

        except Exception as e:
            print(e)
            return None


async def get_account(id_tg: int, action: Literal[None, "dev"] = None) -> Accounts | None:
    async with async_session() as session:
        try:
            if action == "dev":
                account = await session.execute(
                    select(Accounts)
                    .where(Accounts.id_tg == id_tg)
                )
                return account.scalars().first()
            else:
                account = await session.execute(
                    select(Accounts)
                    .where(Accounts.id_user == id_tg)
                )
                return account.scalars().first()
        except Exception as e:
            print(e)
            return None


async def get_super_admin() -> Accounts | None:
    async with async_session() as session:
        try:
            data = await session.execute(select(Accounts).where(Accounts.status == Status.SUPER_ADMIN.value))
            return data.scalars().first()
        except Exception as e:
            print(e)
            return None


# noinspection PyTypeHints
async def dev_update_status(id_tg: int,
                            status_name: Literal[
                                Status.ADMIN.value,
                                Status.SUPER_ADMIN.value,
                                Status.DISABLE.value,
                                Status.ACTIVE.value
                            ]) -> None:
    async with async_session() as session:
        try:
            user_ex = await session.execute(select(Users).join(Accounts).where(Accounts.id_tg == id_tg))
            user = user_ex.scalars().first()
            statement = select(Accounts).where(Accounts.id_tg == id_tg)
            result = await session.execute(statement)
            account = result.scalar()
            if account.status != status_name:
                account.status = status_name
                await session.commit()
                return f"Пользователь по фамилии {user.surname} следующий статус {status_name}"
            else:
                await session.rollback()
                return "У этого пользователя уже есть эта роль"

        except Exception as e:
            await session.rollback()
            print(e)
            return "ERROR"
