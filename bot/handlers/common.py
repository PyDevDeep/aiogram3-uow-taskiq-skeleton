from typing import Callable

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.database.uow import SQLAlchemyUoW
from bot.tasks.broker import example_background_task

router = Router()


@router.message(CommandStart())
async def cmd_start(
    message: Message, state: FSMContext, uow: SQLAlchemyUoW, _get: Callable[..., str]
):
    """
    Entry point. Demonstrates injection of UoW, i18n, and background task enqueuing.
    """
    if not message.from_user:
        return

    await state.clear()

    # Example of using translation via injected _get function
    welcome_text = _get("welcome-message")

    # Example of database interaction via UoW
    # user = await uow.users.get_by_id(message.from_user.id)
    # if not user:
    #     await uow.users.create(...)
    #     await uow.commit()

    # Enqueue background task
    await example_background_task.kiq(
        user_id=message.from_user.id, action="started_bot"
    )

    await message.answer(welcome_text)
