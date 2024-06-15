from abc import ABC
from typing import Dict, Any, Callable, Awaitable
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message

from src.database.users import User



class RegisterMiddleware(BaseMiddleware, ABC):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        session = data["session"]
        user = await User.get(session, event.from_user.id)

        if user is None:
            await User.add(
                session,
                event.from_user.id,
                event.from_user.full_name
            )

        return await handler(event, data)
