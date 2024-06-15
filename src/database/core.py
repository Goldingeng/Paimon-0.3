from __future__ import annotations

from typing import Type

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncAttrs
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, DeclarativeBase, Mapper

from src.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, future=True, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


def table(table_name: str) -> Type[Base]:
    for c in Base.__subclasses__():
        if c.__tablename__ != table_name:
            continue
        return c


async def setup_database() -> None:
    from . import (
        users,
        characters,
        banner,
        associations
        
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)