from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.users import User
from src.keyboards import banner_markup, menu_markup
from ..utils.apscheduler import get_message_user_photo
from aiogram.types import InputMediaPhoto

from src.keyboards.callback import *
from src.config import trash
from src.database.banner import Banner
from src.database.userCharacters import UserCharacters
from src.database.characters import Characters

from datetime import datetime, timedelta

from random import randint, choice, random

banner_router = Router(name="banner")

@banner_router.message(F.text == "/banner")
async def banner_handler(message: Message, session: AsyncSession) -> None:
    banner = await Banner.banner_locate(session)
    leg = await Characters.get(session, banner.main_characters)

    start_time = datetime.fromtimestamp(banner.date_banner)
    end_time = start_time + timedelta(seconds=259200)
    time_remaining = end_time - datetime.now()

    days = time_remaining.days
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    remaining_time_str = f"{days} day, {hours} hour(s), {minutes} minute(s)"

    message_text = (
        f"<b>Звезда баннера - {leg.name}</b>\n\n"
        f"<b>Эпические персонажи</b>\n{await Characters.epicCharacterText(session, banner.epic_characters)}\n\n"
        f"⏳<b>До завершения баннера:</b> {remaining_time_str}⏳"
    )

    await message.answer_photo(leg.photo,
                               message_text,
                               reply_markup=banner_markup(message.from_user.id), parse_mode="HTML")

@banner_router.callback_query(ProfileCallback.filter())
async def profile_callback_handler(
    query: CallbackQuery, session: AsyncSession) -> None:
    data = ProfileCallback.unpack(query.data)
    if data.user_id != query.from_user.id:
        await query.answer("Это не твоя паймон, жулик!", True)
        return
    
    user = await User.get(session=session, user_id=query.from_user.id)
    lvlwallet = await user.lvlwallet_os(session, query.from_user.id)

    
    await query.message.edit_media(InputMediaPhoto(media=await get_message_user_photo(query)))
    await query.message.edit_caption(caption=
        f"<b>{user.nickname}</b>\n"
        f"{user.status}\n\n"
        f"📈 <b>Уровень мешка</b>: {lvlwallet}\n"
        f"🆔 <code>{user.id}</code>\n\n"
        f"💎 <b>Примогемы</b>:  {user.primgems}\n"
        f"💰 <b>Кэшбек</b>: {user.cashback}\n", 
            reply_markup=menu_markup(query.from_user.id), parse_mode="HTML")


@banner_router.callback_query(HistoryCallback.filter())
async def history_callback_handler(
    query: CallbackQuery, session: AsyncSession) -> None:
    data = HistoryCallback.unpack(query.data)

    if data.user_id != query.from_user.id:
        await query.answer("Это не твоя паймон, жулик!", True)
        return
    
    user = await User.get(session=session, user_id=query.from_user.id)
   
    #await query.message.edit_media(InputMediaPhoto(media="AgACAgIAAxkBAAIB8GYNiUjz44_PBh8Ox2DO7SaPLoLRAALl2zEb09xwSE3MmPVddPSVAQADAgADeQADNAQ"))
    last_leg = "Не было"
    last_epic = "Не было"
    if user.last_leg != -1:
        last_leg = await Characters.get(session, user.last_leg)
    if user.last_epic != -1:
        last_epic = await Characters.get(session, user.last_epic)

    await query.answer(f"{user.nickname}\n"
            f"Последняя легендарка: {last_leg.name if user.last_leg != -1 else last_leg}\n"
            f"Последний эпик: {last_epic.name if user.last_epic != -1 else last_epic}\n\n"
            f"Круток после легендарного: {user.until_leg}\n"
            f"Круток после эпического': {user.until_epic}\n",
            True)

    #await query.message.edit_caption(caption=
            #f"{user.nickname}\n"
            #f"Последняя легендарка: {last_leg.name if user.last_leg != -1 else last_leg}\n"
            #f"Последний эпик: {last_epic.name if user.last_epic != -1 else last_epic}\n\n"
            #f"Круток после легендарного: {user.until_leg}\n"
            #f"Круток после эпического': {user.until_epic}\n",
            #reply_markup=history_markup(query.from_user.id))

async def leg_get(eventLeg: int, last_leg: int) -> int:
    
    standart_leg = [61, 82, 83, 84, 85, 86, 55]
    if last_leg in standart_leg or randint(1, 2) == 1:
        return eventLeg
    else:
        return choice(standart_leg)

async def epic_get(eventEpic, epic) -> int:
    if randint(1, 2) == 1:
        return epic
    else:
        return choice(eventEpic)

async def get_character(session: AsyncSession, user, character_id, rarity: int) -> int:
    if await UserCharacters.check(session, user.id, character_id):
        user.cashback += 500 if rarity == 1 else 50
    else:
        await UserCharacters.add(session, user.id, character_id, rarity)
        await session.commit()
    return character_id

async def twist_mechanism(session: AsyncSession, banner, user):
    epic_standart = await Characters.random_epic(session)
    user.primgems -= 160

    if user.until_leg == 89 or (user.until_leg > 75 and random() < 0.2) or (user.until_leg < 75 and random() < 0.005):
        character = await leg_get(banner.main_characters, user.last_leg)
        user.until_leg = 0
        user.until_epic += 1
        user.last_leg = character
        return await get_character(session, user, character, 1)
    
    if user.until_epic >= 9 or random() < 0.05:
        character = await epic_get(banner.epic_characters, epic_standart.id)
        user.until_epic = 0
        user.until_leg += 1
        user.last_epic = character
        return await get_character(session, user, character, 0)
    
    user.until_leg += 1
    user.cashback += 15
    user.until_epic += 1
    await session.commit()
    return -1

@banner_router.callback_query(TwistCallbackc.filter(F.count == 1))
async def twist(query: CallbackQuery, session: AsyncSession, callback_data: TwistCallbackc) -> None:
    if callback_data.user_id != query.from_user.id:
        await query.answer("Это не твоя паймон, жулик!", True)
        return

    banner = await Banner.banner_locate(session)
    user = await User.get(session, query.from_user.id)

    if await Banner.banner_check(session, banner.id):
        await query.answer("Баннер истек!", True)
        return

    if user.primgems < 160:
        await query.answer("У тебя недостаточно примогемов!", True)
        return

    cashback = user.cashback
    prize = [await twist_mechanism(session, banner, user)]
    await show_prize(query, session, user, prize, cashback)

@banner_router.callback_query(TwistCallbackc.filter(F.count == 10))
async def twists(query: CallbackQuery, session: AsyncSession, callback_data: TwistCallbackc) -> None:
    if callback_data.user_id != query.from_user.id:
        await query.answer("Это не твоя паймон, жулик!", True)
        return

    banner = await Banner.banner_locate(session)
    user = await User.get(session, query.from_user.id)

    if await Banner.banner_check(session, banner.id):
        await query.answer("Баннер истек!", True)
        return

    if user.primgems < 1600:
        await query.answer("У тебя недостаточно примогемов!", True)
        return

    cashback = user.cashback
    prize = [await twist_mechanism(session, banner, user) for _ in range(10)]
    await show_prize(query, session, user, prize, cashback)

async def show_prize(query, session, user, prize, cashback):
    prizes_text = ""
    for item in prize:
        if item == -1:
            prizes_text += f"⚪ {choice(trash)}\n"
        else:
            character = await Characters.get(session, item)
            rar = "🟡" if character.rarity == 1 else "🟣"
            prizes_text += f"{rar} {character.name}\n"

    await query.answer(f"Твоя награда\n\n{prizes_text}\n\nexp: {user.cashback - cashback}🧪", True)
    #await query.message.edit_caption(caption=f"<b>Твоя награда</b>\n\n{prizes_text}\n\nКэшбек: {user.cashback - cashback}💰", reply_markup=banner_markup(query.from_user.id), parse_mode="HTML")

