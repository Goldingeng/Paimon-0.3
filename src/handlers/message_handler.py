import random
import time
import difflib

import asyncio
from aiogram import Router, F
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.users import User
from src.database import core

from src.config import quotes_awards, prim_photo

from src.keyboards import message_markup

message_router = Router(name="message")

user_cache = {}

async def user_record(session: AsyncSession, user_id, last_message_time, message_count, primgems):
    user = await User.get(session, user_id)
    user.dateMess = last_message_time
    user.counterMessage = message_count
    user.primgems += primgems
    await session.commit()

    del user_cache[user_id]

async def issuing_rewards(session: AsyncSession, user_id, last_message_time, primgems):
    user = await User.get(session, user_id)
    user.dateMess = last_message_time
    user.counterMessage = 0
    user.primgems += primgems
    await session.commit()

    del user_cache[user_id]

async def cleanup_inactive_cache():
    while True:
        current_time = int(time.time())
        inactive_users = [user_id for user_id, data in user_cache.items() if current_time - data["last_message_time"] >= 300]
        for user_id in inactive_users:

            async with core.async_session() as session:
                await user_record(session,
                            user_id,
                            user_cache[user_id]["last_message_time"], 
                            user_cache[user_id]["message_count"],
                            0)
    
        await asyncio.sleep(30)



async def increasing_message_counter(user_id, last_message_time, message_count, text):
    user_cache[user_id]["last_message_time"] = int(time.time())
    user_cache[user_id]["message_count"] += 1
    user_cache[user_id]["text"] = text


async def is_message_valid(message: Message, user_cache: dict, user_id: int) -> bool:
    if message.chat.id == user_id:
        return False

    previous_message = user_cache.get("text")
    current_message = message.text
    similarity = difflib.SequenceMatcher(None, previous_message, current_message).ratio()
    if similarity > 0.6:
        return False


    if len(current_message) < 2:
        return False


    last_message_time = user_cache.get("last_message_time")
    if int(time.time()) - last_message_time < 15:
        return False

    return True

async def answer_gen(nick, message_count, primgems):
    text =  f"""<b>{random.choice(quotes_awards)}!</b>

<b>{nick}</b>
Только что отправил <b>💬{message_count}💬</b> сообщение и споймал свою звезду пути!

На вашем небе появилось <b>✨{primgems}✨</b> примогемов! 💫"""
    return text



@message_router.message(F.text)
async def message_handler(message: Message, session: AsyncSession) -> None:
    user_id = message.from_user.id

    if user_id in user_cache:
        user_data = user_cache[user_id]
        last_message_time = user_data.get("last_message_time")
        message_count = user_data.get("message_count")
        text = user_data.get("text")
    else:
        user = await User.get(session=session, user_id=message.from_user.id)
        last_message_time = user.dateMess
        message_count = user.counterMessage
        text = message.text
        user_cache[user_id] = {"last_message_time": last_message_time, "message_count": message_count, "text": text,}
    
    if await is_message_valid(message, user_cache[user_id], user_id):
        message_count = int(user_cache[user_id].get("message_count")) + 1
        if message_count >= 100:
            chance = min(5 + (message_count - 100) * 0.5, 100)
            if message_count >= 150 or random.randint(1, 100) <= chance:
                user = await User.get(session, user_id) 
                lvlWallet = user.lvlWallet  
                primgems = message_count * lvlWallet
                await issuing_rewards(session, user_id, last_message_time, primgems)
                await message.answer_photo(prim_photo, await answer_gen(user.nickname, message_count, primgems), "HTML", reply_markup=message_markup(user_id))
            else:
                await increasing_message_counter(user_id, last_message_time, message_count, message.text)
        else:
            await increasing_message_counter(user_id, last_message_time, message_count, message.text)
    
