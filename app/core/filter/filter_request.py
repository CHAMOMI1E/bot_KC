from app.db.models import Accounts, async_session, Status
from sqlalchemy import select


async def search_admin(id_tg) -> Accounts | None:
    async with async_session() as session:
        try:
            blocks = await session.execute(
                select(Accounts)
                .where(Accounts.status.in_([Status.ADMIN.value, Status.SUPER_ADMIN.value, Status.DEVELOPER.value]))
                .where(Accounts.id_tg == id_tg)
            )
            return blocks.scalars().first()
        except Exception as e:
            print(e)
            return None


async def search_super_admin(id_tg) -> Accounts | None:
    async with async_session() as session:
        try:
            blocks = await session.execute(
                select(Accounts)
                .where(Accounts.status.in_([Status.SUPER_ADMIN.value, Status.DEVELOPER.value]))
                .where(Accounts.id_tg == id_tg)
            )
            return blocks.scalars().first()
        except Exception as e:
            print(e)
            return None


async def search_developer(id_tg) -> Accounts | None:
    async with async_session() as session:
        try:
            blocks = await session.execute(
                select(Accounts)
                .where(Accounts.status == Status.DEVELOPER.value)
                .where(Accounts.id_tg == id_tg)
            )
            return blocks.scalars().first()
        except Exception as e:
            print(e)
            return None
