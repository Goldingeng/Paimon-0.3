from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from sqlalchemy.ext.asyncio import AsyncSession

from ..utils.apscheduler import get_message_user_photo

from src.database.users import User

from src.keyboards import pumping_markup

from src.keyboards.callback import *

pumping_router = Router(name="pumping")

try:
    @pumping_router.message(F.text == "/pumping")
    async def pumping_handler(message: Message, session: AsyncSession) -> None:
        user = await User.get(session=session, user_id=message.from_user.id)
        lvlwallet = await user.lvlwallet_os(session, message.from_user.id)

        if lvlwallet == "1":
            price = 5000

        if lvlwallet == "2":
            price = 10000

        if lvlwallet == "3":
            price = "Max"
 
            
        await message.answer_photo(
            await get_message_user_photo(message),
            f"<b>{user.nickname}</b>\n"
            f"{user.status}\n\n"
            f"📈 <b>Уровень мешка</b>: {lvlwallet} ({price})\n"
            f"🆔 <code>{user.id}</code>\n\n"
            f"💰 <b>Кэшбек</b>: {user.cashback}\n",
            parse_mode="HTML", 
            reply_markup=pumping_markup(message.from_user.id)
        )
except Exception as e:
    print(e)


try:
    @pumping_router.callback_query(BagCallbackc.filter())
    async def history_callback_handler(
        query: CallbackQuery, session: AsyncSession) -> None:
        data = BagCallbackc.unpack(query.data)

        if data.user_id != query.from_user.id:
            await query.answer("Это не твоя паймон, жулик!", True)
            return

        user = await User.get(session, query.from_user.id)
        lvlwallet = await user.lvlwallet_os(session, query.from_user.id)

        if lvlwallet == "3":
            await query.answer("У тебя максимальный уровень мешка! Куда больше?)", True)
            return
        
        if lvlwallet == "1":
            price = 5000

        if lvlwallet == "2":
            price = 10000


        if user.cashback < price:
            await query.answer("У тебя недостаточно кэшбека!", True)

            return

        user.cashback -= price
        user.lvlWallet += 2
        await session.commit()

        await query.answer("Успешно!", True)

except Exception as e:
    print(e)

