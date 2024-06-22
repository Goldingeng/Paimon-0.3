from aiogram import Router, F
from aiogram.types import Message

from src.config import bot_prew

from src.keyboards import help_markup

help_router = Router(name="help")

@help_router.message(F.text.startswith("/start"))
async def help_handler(message: Message) -> None:
    await message.answer_photo(
bot_prew,
"""<b>Приветик!</b>

Это игровой бот <b>'Симулятор круток'</b>, как можно понять по названию, предназначенный для <i>развлекательных целей</i>.

<b>Вот имеющиеся основные команды:</b>
<code>/menu</code>
<code>/rename</code> 'Новый ник'
<code>/restatus</code> 'Новый статус'
<code>/promo</code> 'Промокод'
<i>Баннер с героем обновляется каждые 3 дня, система гарантов как в самой игре, а валюта получается путем общения в групповых чатах. При получении награды бот тебе об этом сообщит!</i>""",
parse_mode="HTML",
reply_markup=help_markup()
    )

@help_router.message(F.text.startswith("/help"))
async def help_handler(message: Message) -> None:
    await message.answer_photo(
bot_prew,
"""<b>Приветик!</b>

Это игровой бот <b>'Симулятор круток'</b>, как можно понять по названию, предназначенный для <i>развлекательных целей</i>.

<b>Вот имеющиеся основные команды:</b>
<code>/menu</code>
<code>/rename</code> 'Новый ник'
<code>/restatus</code> 'Новый статус'
<code>/promo</code> 'Промокод'
<i>Баннер с героем обновляется каждые 3 дня, система гарантов как в самой игре, а валюта получается путем общения в групповых чатах. При получении награды бот тебе об этом сообщит!</i>""",
parse_mode="HTML",
reply_markup=help_markup()
    )