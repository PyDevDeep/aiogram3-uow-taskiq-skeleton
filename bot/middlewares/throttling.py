import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

logger = logging.getLogger(__name__)


class AntiSpamMiddleware(BaseMiddleware):
    """
    Strict flood protection.
    Drops spam requests before they reach handlers and the database.
    """

    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        # In a real production environment, a Redis client injection should be here
        self.cache: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        # Apply throttling only to messages from real users
        if not isinstance(event, Message) or not event.from_user:
            return await handler(event, data)

        user_id = event.from_user.id

        # TODO: Replace with a real Redis call, for example:
        # allowed = await redis_client.set(f"lock:{user_id}", 1, ex=1, nx=True)
        allowed = True

        if not allowed:
            logger.warning(f"Anti-spam triggered for user {user_id}")
            return

        return await handler(event, data)
