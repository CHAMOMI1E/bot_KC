from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncAttrs

from enum import Enum

from typing import Annotated, List

bigint = Annotated[int, "BigInteger"]

engine = create_async_engine("postgresql+asyncpg://postgres:02082002@localhost:5433/test_db", echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Status(Enum):
    ACTIVE = "ACTIVE"
    DISABLE = "DISABLE"
    ADMIN = "ADMIN"
    UNKNOWN = "UNKNOWN"


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[bigint] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    patronymic: Mapped[str] = mapped_column()
    # departament: Mapped[str] = mapped_column()

    accounts: Mapped[List["Accounts"]] = relationship("Accounts", back_populates="user")


class Accounts(Base):
    __tablename__ = 'accounts'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_tg: Mapped[bigint] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column()
    id_user: Mapped[bigint] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped[List["Users"]] = relationship(
        "Users", back_populates="accounts"
    )

    __table_args__ = (UniqueConstraint('id_tg', 'id_user'),)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
