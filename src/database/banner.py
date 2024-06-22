import time
from typing import Union, List

from sqlalchemy import select, BigInteger, Column
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.dialects.postgresql import ARRAY

from src.database.core import Base

class Banner(Base):
    __tablename__ = "banners"
    __allow_unmapped__ = True

    id: int = Column(
        BigInteger,
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True
    )

    main_characters: int = Column(BigInteger)
    epic_characters: List[int] = Column(ARRAY(BigInteger), nullable=True)
    date_banner: int = Column(BigInteger, 
                              default=int(time.time()))
    twists_produced: int = Column(BigInteger, 
                                  default=0)
    winnings: int = Column(BigInteger, 
                           default=0)
    relevance: bool = Column(BigInteger, 
                             default=1)

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> 'Banner':
        banner_query = select(cls).filter(cls.id == id)
        return await session.scalar(banner_query)
    
    #Добавить баннер
    @classmethod
    async def add(cls, session: AsyncSession, main_characters: int, epic_characters: int) -> 'None':
        banner = cls(main_characters=main_characters, epic_characters=epic_characters)
        
        session.add(banner)
        await session.commit()

    #Сменить актуальность баннера на "False"
    @classmethod
    async def relevance_off(cls, session: AsyncSession) -> None:
        stm = select(cls).filter(cls.relevance == 1)
        banners = await session.scalars(stm)
        
        for banner in banners:

            banner.relevance = 0

        await session.commit()

    #Проверка баннера на время
    @classmethod
    async def banner_check(cls, session: AsyncSession, id: int) -> Union[bool, str]:
        date_banner = (await Banner.get(session=session, id = id)).date_banner
        if time.time() - date_banner > 259200:
            return True
        
    #Достать актуальный баннер
    @classmethod
    async def banner_locate(cls, session: AsyncSession) -> "Banner":
        banner = select(cls).filter(cls.relevance == 1)

        return await session.scalar(banner)

    