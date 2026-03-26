import logging
import traceback

from aiogram import Router, types

logger = logging.getLogger(__name__)
router = Router()


@router.errors()
async def global_error_handler(event: types.ErrorEvent):
    """Centralized fatal error interceptor."""
    logger.error(f"Error during update processing: {event.exception}")
    logger.error(traceback.format_exc())

    if event.update.message:
        await event.update.message.answer(
            "⚙️ Internal server error. Please try again later."
        )
