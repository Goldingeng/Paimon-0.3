from aiogram import Router, F
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession
from src.database.users import User


nick_router = Router(name="rename")

@nick_router.message(F.text.startswith("/rename"))
async def nick_handler(message: Message, session: AsyncSession) -> None:

    nickname = message.text[len("/rename"):].strip()
    valid_nickname = ''.join(e for e in nickname if e.isalnum() or e.isspace())[:90]

    if not valid_nickname:
        await message.answer("Некорректный ник. Попробуйте другой.")
    else:
        user = await User.get(session, message.from_user.id)
        user.nickname = valid_nickname
        await session.commit()
        
        await message.answer(f"Ваш ник изменен на: {valid_nickname}")


