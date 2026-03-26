from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User


class I18nMiddleware(BaseMiddleware):
    """Stub for i18n middleware to extract locale and inject translation function."""

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        user: User | None = data.get("event_from_user")
        # Default fallback language
        locale = "en"

        if user and user.language_code:
            locale = user.language_code

        # This should connect to fluent.runtime or similar translator instance
        # Dummy implementation for architectural skeleton
        def _get(key: str, **kwargs: Any) -> str:
            return f"[{locale}] {key}"

        data["_get"] = _get
        data["locale"] = locale

        return await handler(event, data)
