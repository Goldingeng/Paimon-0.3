from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.types import Message


from src.config import avatar_photo
scheduler = AsyncIOScheduler()

async def get_message_user_photo(message: Message) -> str:
    
    user_photos = await message.bot.get_user_profile_photos(message.from_user.id)

    photo = user_photos.photos[0][1].file_id if user_photos.photos else avatar_photo

    return photo