from aiogram import Router, F, Bot, types
from aiogram.types import user_profile_photos
from aiogram.types import Message, CallbackQuery
from aiogram.types import InputMediaPhoto

from sqlalchemy.ext.asyncio import AsyncSession

from ..utils.apscheduler import get_message_user_photo

from src.database.users import User
from src.keyboards import menu_markup, banner_markup, characters_markup

from .banner_handler import banner_handler


from src.keyboards.callback import *

from src.database.characters import Characters
from src.database.userCharacters import UserCharacters
from src.database.banner import Banner

from datetime import datetime, timedelta

from aiogram.types import InputMediaPhoto

menu_router = Router(name="menu")



@menu_router.message(F.text == "/menu")
async def menu_handler(message: Message, session: AsyncSession) -> None:
    user = await User.get(session=session, user_id=message.from_user.id)
    lvlwallet = await user.lvlwallet_os(session, message.from_user.id)
        
    await message.answer_photo(
        await get_message_user_photo(message),
        f"<b>{user.nickname}</b>\n"
        f"{user.status}\n\n"
        f"📈 <b>Уровень мешка</b>: {lvlwallet}\n"
        f"🆔 <code>{user.id}</code>\n\n"
        f"💎 <b>Примогемы</b>:  {user.primgems}\n"
        f"💰 <b>Кэшбек</b>: {user.cashback}\n", 
        reply_markup=menu_markup(message.from_user.id), parse_mode="HTML", 
    )


@menu_router.callback_query(BannerCallback.filter())
async def banner_callback_handler(query: CallbackQuery, session: AsyncSession) -> None:

    data = BannerCallback.unpack(query.data)

    if data.user_id != query.from_user.id:
        await query.answer("Это не твоя паймон, жулик!", True)
        return
    
    data = BannerCallback.unpack(query.data)
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
    

    await query.message.edit_media(InputMediaPhoto(media=leg.photo))
    await query.message.edit_caption(caption=message_text, reply_markup=banner_markup(query.from_user.id))


@menu_router.callback_query(CharactersCallbackc.filter())
async def characters_callback_handler(query: CallbackQuery, session: AsyncSession) -> None:
    data = CharactersCallbackc.unpack(query.data)
    user_id = query.from_user.id

    if data.user_id != user_id:
        await query.answer("Это не твоя паймон, жулик!", True)
        return

    page = data.page if data.page else 0
    if page == -404:
        await query.answer("Дальше дороги нет!", True)
        return  
    print(page)
    print(data)

    # Проверка наличия персонажей на текущей странице
    user_characters = await UserCharacters.get_characters(session, user_id, offset=page * 10, limit=10)

    characters_info = []
    last =True
    for user_character in user_characters:
        last = False
        character = await Characters.get(session, user_character.character_id)
        rarity_symbol = "🟡" if character.rarity == 1 else "🟣"
        characters_info.append(
            f"{rarity_symbol} {character.name}"
        )
    if last:
        await query.answer("Дальше дороги нет!", True)
        return  
    characters_info.sort()

    characters_text = "\n".join(characters_info)

    markup = characters_markup(user_id, page)

    await query.message.edit_caption(
        caption=f"Ваши персонажи (страница {page + 1}):\n\n{characters_text}\n",
        reply_markup=markup
    )

@menu_router.callback_query(PumpingCallbackc.filter())
async def pumping_callback_handler(query: CallbackQuery, session: AsyncSession) -> None:
    
    data = PumpingCallbackc.unpack(query.data)

    if data.user_id != query.from_user.id:
        await query.answer("Это не твоя паймон, жулик!", True)
        return

    
    await query.message.edit_caption(caption="[eq cjcb]")