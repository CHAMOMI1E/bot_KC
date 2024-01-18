from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint, Column, String
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, AsyncAttrs

from enum import Enum

from typing import Annotated, List

bigint = Annotated[int, "BigInteger"]

engine = create_async_engine("postgresql+asyncpg://postgres:02082002@localhost:5433/test_db", echo=True)

async_session = async_sessionmaker(engine)


class Status(Enum):
    ACTIVE = "ACTIVE"
    DIZABLE = "DIZABLE"
    ADMIN = "ADMIN"
    UNKNOWN = "UNKNOWN"


class Base(AsyncAttrs, DeclarativeBase):
    pass


# class User(Base):
#     __tablename__ = "users"
#
#     id = Column(BigInteger, primary_key=True)
#     name = Column(String)
#     surname = Column(String)
#     patronymic = Column(String)
#
#     accounts = relationship("Account", back_populates="user")
#
#
# class Account(Base):
#     __tablename__ = 'accounts'
#
#     id = Column(BigInteger, primary_key=True)
#     id_tg = Column(BigInteger)
#     status = Column(String)
#     id_user = Column(BigInteger, ForeignKey("users.id"))
#
#     user = relationship("User", back_populates="accounts")
#
#     __table_args__ = (UniqueConstraint('id_tg', 'id_user'),)


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
