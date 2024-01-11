from app.db.models import User, async_session
from sqlalchemy import select


async def get_user():
    async with async_session() as session:
        result = await session.scalar(select(User))
        return result
