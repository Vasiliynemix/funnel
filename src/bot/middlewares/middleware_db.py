from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.bot.structures.data_structure import TransferData
from src.db.database import Database


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        async_session_factory = async_sessionmaker(
            bind=data["engine"], class_=AsyncSession, expire_on_commit=False
        )
        async with async_session_factory() as session:
            data["db"] = Database(session)
            await data["db"].user.update_at(user_id=event.from_user.id)
            return await handler(event, data)
