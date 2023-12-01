from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.db.database import Database


class EndFilter(BaseFilter):
    async def __call__(self, message: Message, db: Database):
        user = await db.user.get_by_user_id(user_id=message.from_user.id)
        if user.end_answer:
            return False
        return True
