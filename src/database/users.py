import time
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import select, BigInteger, Column, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from src.database.core import Base

if TYPE_CHECKING:
    from src.database.characters import Characters


class User(Base):
    __tablename__ = "Users"
    __allow_unmapped__ = True

    id: int = Column(
        BigInteger,
        primary_key=True,
        index=True,
        unique=True
    )

    nickname: str = Column(String)

    status: str = Column(String, default="Вперед, к звездам!")

    counterMessage: str = Column(BigInteger,
                                 default=0)
    primgems: int = Column(BigInteger,
                           default=0)
    cashback: int = Column(BigInteger,
                           default=0)
    dateMess: str = Column(BigInteger,
                           default=int(time.time()))
    lvlWallet: int = Column(BigInteger,
                            default=12)
    last_epic: str = Column(BigInteger,
                            default=-1)
    last_leg: str = Column(BigInteger,
                           default=-1)
    until_epic: int = Column(BigInteger,
                             default=0)
    until_leg: int = Column(BigInteger,
                            default=0)


    @classmethod
    async def get(cls, session: AsyncSession, user_id: int) -> 'User':
        user_query = select(cls).filter(cls.id == user_id)
        return await session.scalar(user_query)

    @classmethod
    async def add_characters(cls, session: AsyncSession, user_id: int, id: int) -> None:
        user = 6

    @classmethod
    async def add(cls, session: AsyncSession, user_id: int, nickname: str) -> 'User':
        user = await cls.get(session, user_id)

        if user is None:
            user = cls(id=user_id, nickname=nickname)
            session.add(user)
            await session.commit()

        return user
    
    @classmethod
    async def lvlwallet_os(cls, session: AsyncSession, user_id: int) -> str:
        user = await cls.get(session, user_id)
        if user.lvlWallet == 12:
            return "1"
        if user.lvlWallet == 14:
            return "2"
        else:
            return "3"
        
    @classmethod
    async def change_nickname(cls, session: AsyncSession, user_id: int, new_nickname: str) -> 'User':
        user = await cls.get(session, user_id)
        if user:
            user.nickname = new_nickname
            await session.commit()


    @classmethod
    async def change_status(cls, session: AsyncSession, user_id: int, new_status: str) -> 'User':
        user = await cls.get(session, user_id)
        if user:
            user.status = new_status
            await session.commit()


    @classmethod
    async def change_lvlwallet(cls, session: AsyncSession, user_id: int, new_lvlwallet: int, price: int) -> 'User':
        user = await cls.get(session, user_id)
        if user:
            user.lvlWallet = new_lvlwallet
            user.primgems += price
            await session.commit()

    @classmethod
    async def change_last_epic(cls, session: AsyncSession, user_id: int, new_last_epic: str) -> 'User':
        user = await cls.get(session, user_id)
        if user:
            user.last_epic = new_last_epic
            user.until_epic += 1
            await session.commit()

    @classmethod
    async def change_last_leg(cls, session: AsyncSession, user_id: int, new_last_leg: str) -> 'User':
        user = await cls.get(session, user_id)
        if user:
            user.last_leg = new_last_leg
            user.last_leg += 1
            await session.commit()
