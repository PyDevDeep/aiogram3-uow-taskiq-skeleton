from taskiq_redis import ListQueueBroker

from bot.core.config import settings

# Setup Redis broker for background task execution
broker = ListQueueBroker(
    url=settings.redis_url,
)


@broker.task
async def example_background_task(user_id: int, action: str) -> None:
    """
    Example of an isolated background task.
    Do not place heavy business logic directly here, use services.
    """
    import logging

    logger = logging.getLogger(__name__)
    logger.info(f"Executing task for user {user_id}: {action}")
