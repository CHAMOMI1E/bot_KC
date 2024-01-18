from app.db.models import Users, Accounts, async_session, Status
from sqlalchemy import select


async def get_users():
    async with async_session() as session:
        result = await session.scalar(select(Users)).all()
        return result


async def add_user(name: str, surname: str, patronymic: str, id_tg: int) -> None:
    async with async_session() as session:
        try:
            # создание экземпляра пользователя
            new_user = Users(name=name, surname=surname, patronymic=patronymic)
            session.add(new_user)
            session.flush()  # чтобы получить id пользователя

            # создание экземпляра аккаунта
            new_account = Accounts(id_tg=id_tg, status=Status.UNKNOWN, id_user=new_user.id)
            session.add(new_account)

            session.commit()  # сохранение изменений в базе данных

        except Exception as e:
            print("Error adding user info:", e)
            session.rollback()
        # return
