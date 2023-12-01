from typing import TypedDict

from aiogram import Bot
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.db.database import Database
from src.db.models import User


class TransferData(TypedDict):
    engine: AsyncEngine
    db: Database
    bot: Bot
    user: User
