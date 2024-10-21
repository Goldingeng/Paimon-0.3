from aiogram import Router, F
from aiogram.types import Message


from sqlalchemy.ext.asyncio import AsyncSession

from src.database.characters import Characters

moder_router = Router(name="add")

@moder_router.message(lambda message: message.chat.id == 1167542251)
async def menu_handler(message: Message, session: AsyncSession) -> None:
    if message.text:
        return

    lines = message.caption.split('\n')
    

    if len(lines) == 3:
        name = lines[1]
        rarity = lines[2]
        photo_id = message.photo[0].file_id if int(rarity) == 1 else None
        
        await Characters.add(
            session,
            name=name,
            rarity=int(rarity),
            photo=photo_id
        )
        await message.answer("Успешно!")
    else:
        await message.answer("Invalid format. Please provide character information in the correct format.")


