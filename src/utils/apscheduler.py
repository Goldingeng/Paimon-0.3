from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import Message, CallbackQuery


from src.config import fallback_photo
scheduler = AsyncIOScheduler()

async def get_message_user_photo(message: Message) -> str:
    
    user_photos = await message.bot.get_user_profile_photos(message.from_user.id)
    photo = user_photos.photos[0][1].file_id if user_photos.photos else fallback_photo

    return photo