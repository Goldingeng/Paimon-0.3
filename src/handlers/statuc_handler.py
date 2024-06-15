from aiogram import Router, F, Bot, types
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.users import User



status_router = Router(name="status")

@status_router.message(F.text.startswith("/status"))
async def status_handler(message: Message, session: AsyncSession) -> None:

    status = message.text[len("/status"):].strip()

    valid_status = ''.join(e for e in status if e.isalnum() or e.isspace())[:90]
    
    if not valid_status:
        await message.answer("Некорректный статус. Попробуйте другой.")
    else:
        user = await User.get(session, message.from_user.id)
        user.status = valid_status
        await session.commit()
        
        await message.answer(f"Ваш статус изменен на: {status}")