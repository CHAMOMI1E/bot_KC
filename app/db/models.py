from sqlalchemy import BigInteger, String
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncAttrs

engine = create_async_engine("sqlite+aiosqlite:///db.sqlite3", echo=True)

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    tg_id: mapped_column(BigInteger)
    status: Mapped[str] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
