from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.base import Base


class User(Base):
    """Declarative SQLAlchemy model for the users table."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    language_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
