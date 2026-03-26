from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models.user import User


class UserRepository:
    """
    Isolated data access layer for the User model.
    Never commit transactions here. UoW handles commits.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_tg_id(self, telegram_id: int) -> User | None:
        """Fetch user by Telegram ID."""
        stmt = select(User).where(User.telegram_id == telegram_id)
        return (await self.session.execute(stmt)).scalar_one_or_none()

    async def create(self, telegram_id: int, language_code: str | None = None) -> User:
        """Create a new user. Uses flush to get the generated ID immediately."""
        user = User(telegram_id=telegram_id, language_code=language_code)
        self.session.add(user)
        await self.session.flush()
        return user
