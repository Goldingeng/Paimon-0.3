from src.database.banner import Banner
from src.database.characters import Characters
from src.database import core
from asyncio import sleep

async def change_banner_periodically():
    async with core.async_session() as session:
        while True:
            
            await Banner.relevance_off(session)

            leg = await Characters.select_leg(session)
            epic = await Characters.select_epic(session)
            epic = [v.id for v in epic]
            ordinary = [61, 82, 83, 84, 85, 86, 55]

            if leg in ordinary:
                leg = await Characters.select_leg(session)
            await Banner.add(session, leg.id, epic)
            await Characters.banner_history_up(session, leg.id, epic)

            await sleep(259200) 