from enum import Enum
from datetime import datetime
from typing_extensions import Annotated, List
from config import DB_TOKEN

from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

bigint = Annotated[int, "BigInteger"]

engine = create_async_engine(DB_TOKEN,
                             echo=False)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Status(Enum):
    ACTIVE = "ACTIVE"
    DISABLE = "DISABLE"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"
    DEVELOPER = "DEVELOPER"
    UNKNOWN = "UNKNOWN"


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"

    id: Mapped[bigint] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    surname: Mapped[str] = mapped_column()
    patronymic: Mapped[str] = mapped_column()

    accounts: Mapped[List["Accounts"]] = relationship("Accounts", back_populates="user")


class Accounts(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_tg: Mapped[bigint] = mapped_column(BigInteger)
    status: Mapped[str] = mapped_column()
    id_user: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    user: Mapped[List["Users"]] = relationship("Users", back_populates="accounts")

    __table_args__ = (UniqueConstraint("id_tg", "id_user"),)


class Statistics(Base):
    __tablename__ = "statistics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name_of_action: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
