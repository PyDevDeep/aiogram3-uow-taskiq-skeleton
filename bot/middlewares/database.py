from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.database.session import async_session_maker
from bot.database.uow import SQLAlchemyUoW


class DatabaseMiddleware(BaseMiddleware):
    """Injects Unit of Work into the handler's context data."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Provide UoW instance to the handler
        async with SQLAlchemyUoW(async_session_maker) as uow:
            data["uow"] = uow
            return await handler(event, data)
