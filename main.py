import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.config import TOKEN
from src.database import setup_database, async_session
from src.handlers import all_routers
from src.middlewares.database_middleware import DatabaseMiddleware
from src.middlewares.register_middleware import RegisterMiddleware
from src.utils.apscheduler import scheduler
from src.utils.swith_banner import change_banner_periodically
from src.handlers.message_handler import cleanup_inactive_cache

logging.basicConfig(
    format=u'[%(filename)+13s][LINE:%(lineno)-3s][%(asctime)s] %(message)s',
    level=logging.WARNING
)

async def main() -> None:
    await setup_database()
    session = async_session()
    scheduler.start()
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML,
            allow_sending_without_reply=True,
            link_preview_is_disabled=True
        )
    )
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.message.middleware(DatabaseMiddleware(session))
    dp.callback_query.middleware(DatabaseMiddleware(session))
    dp.message.middleware(RegisterMiddleware())
    dp.include_routers(*all_routers)

    logging.warning("Bot successfuly started.")
    await dp.start_polling(bot, handle_as_tasks=False)

    logging.warning("Bot shtting down...")
    await session.close_all()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(cleanup_inactive_cache())
    loop.create_task(change_banner_periodically())
    loop.run_until_complete(main())
