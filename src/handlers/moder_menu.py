from aiogram import Router, F
from aiogram.types import Message


from sqlalchemy.ext.asyncio import AsyncSession

from src.database.characters import Characters

moder_router = Router(name="add")

@moder_router.message(lambda message: message.chat.id == 1167542251)
async def menu_handler(message: Message, session: AsyncSession) -> None:
    if message.text:
        return
    
    if lambda message: "/add" in message.caption != True:
        return

    # Разбиваем подпись на строки
    lines = message.caption.split('\n')
    
    # Проверяем, есть ли три строки (для имени, редкости и истории на баннере)
    if len(lines) == 3:
        # Получаем данные из строк
        name = lines[1]
        rarity = lines[2]
        
        # Определяем фото в зависимости от редкости персонажа
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


