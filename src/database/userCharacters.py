from typing import TYPE_CHECKING, List

from sqlalchemy import select, Column, Integer, BigInteger
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import Base

from sqlalchemy import desc

class UserCharacters(Base):
    __tablename__ = "userCharacters"
    __allow_unmapped__ = True

    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True
    )

    user_id: int = Column(BigInteger)
    character_id: int = Column(BigInteger)
    rarity: int = Column(Integer)

    @classmethod
    async def add(cls, session: AsyncSession, user_id: int, character_id: int, rarity: int) -> None:
        userCharacters = cls(user_id=user_id, character_id=character_id, rarity=rarity)
        session.add(userCharacters)
        await session.commit()

    @classmethod
    async def check(cls, session: AsyncSession, user_id: int, character_id: int) -> bool:
        query = select(cls).filter_by(user_id=user_id, character_id=character_id)
        result = await session.execute(query)
        return result.scalar() is not None

    @classmethod
    async def get_characters(cls, session: AsyncSession, user_id: int, offset: int = 0, limit: int = 10) -> List['UserCharacters']:
        query = select(cls).filter_by(user_id=user_id).order_by(desc(cls.rarity)).offset(offset).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_total_characters(cls, session: AsyncSession, user_id: int, offset: int = 0, limit: int = 10) -> List['UserCharacters']:
        query = select(cls).filter_by(user_id=user_id).order_by(desc(cls.rarity)).offset(offset)
        result = await session.execute(query)
        return result.scalars().all()