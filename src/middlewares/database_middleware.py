import asyncio
from abc import ABC
from typing import Dict, Any, Callable, Awaitable
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message
from aiogram.types.base import TelegramObject
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class DatabaseMiddleware(BaseMiddleware, ABC):
    def __init__(self, session: AsyncSession):
        super().__init__()
        self._session = session

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        data["session"] = self._session
        return await handler(event, data)
