from aiogram import Router, F, Bot, types
from aiogram.types import user_profile_photos
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputMediaPhoto

from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.filters.callback_data import CallbackData
from src.database.users import User
from src.database.characters import Characters

nick_router = Router(name="nick")

@nick_router.message(F.text.startswith("/nick"))
async def nick_handler(message: Message, session: AsyncSession) -> None:

    nickname = message.text[len("/nick"):].strip()

    valid_nickname = ''.join(e for e in nickname if e.isalnum() or e.isspace())[:90]

    if not valid_nickname:
        await message.answer("Некорректный ник. Попробуйте другой.")
    else:
        user = await User.get(session, message.from_user.id)
        user.nickname = valid_nickname
        await session.commit()
        
        await message.answer(f"Ваш ник изменен на: {valid_nickname}")


