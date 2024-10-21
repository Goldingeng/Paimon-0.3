from typing import List

from sqlalchemy import Sequence, select, Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core import Base
from sqlalchemy import and_, not_
from sqlalchemy import func

class Characters(Base):
    __tablename__ = "characters"
    __allow_unmapped__ = True

    id: int = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True
    )

    name: str = Column(String)
    rarity: int = Column(Integer)
    photo: str = Column(String)
    banner_history: int = Column(Integer, default=0)

    @classmethod
    async def get(cls, session: AsyncSession, character_id: int) -> 'Characters':
        character_query = select(cls).filter_by(id=character_id)
        return await session.scalar(character_query)

    @classmethod
    async def get_all(cls, session: AsyncSession, offset: int = 0, limit: int = 1000) -> Sequence['Characters']:
        character_query = select(cls).offset(offset).limit(limit)
        return (await session.scalars(character_query)).all()

    @classmethod
    async def add(
            cls,
            session: AsyncSession,
            name: str,
            rarity: int,
            photo: str,
            
    ) -> 'Characters':
        character = cls(
            name=name,
            rarity=rarity,
            photo=photo,

        )
        session.add(character)
        await session.commit()
        return character

    @classmethod
    async def select_leg(cls, session: AsyncSession) -> "Characters":
        ordinary = [61, 82, 83, 84, 85, 86, 55]
        legends = (
            select(cls)
            .filter(and_(cls.rarity == 1, not_(cls.id.in_(ordinary))))
            .order_by(cls.banner_history)
            .limit(5)
            .order_by(func.random())
            .limit(1)
        )
        
        return await session.scalar(legends)

    @classmethod
    async def select_epic(cls, session: AsyncSession) -> List["Characters"]:
        epics = (
            select(cls)
            .filter_by(rarity=0)
            .order_by(cls.banner_history)
            .limit(10)
            .order_by(func.random())
            .limit(4)
        )

        return await session.scalars(epics)

    @classmethod
    async def random_epic(cls, session: AsyncSession) -> "Characters":
        epic = select(cls).filter_by(rarity=0).order_by(func.random())

        return await session.scalar(epic)

    @classmethod
    async def banner_history_up(cls, session: AsyncSession, legid: int, epicId: List) -> None:
        getLegCharacter = select(cls).filter(cls.id == legid)
        legCharacter = await session.scalar(getLegCharacter)
        legCharacter.banner_history += 1

        for id in epicId:
            getEpicCharacter = select(cls).filter(cls.id == id)
            epicCharacter = await session.scalar(getEpicCharacter)

            epicCharacter.banner_history += 1

        await session.commit()


    @classmethod
    async def epicCharacterText(cls, session: AsyncSession, epics: List) -> str:
        names = []
        for epic in epics:
            characters = select(cls).filter(cls.id == epic)
            name = await session.scalar(characters)
            names.append("🟣 " + name.name)

        return "\n".join(names)
