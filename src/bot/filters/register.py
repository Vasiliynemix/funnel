from aiogram.filters import BaseFilter
from aiogram.types import Message

from src.bot.filters.utils.is_admin import is_admin
from src.bot.structures.role import Role
from src.db.database import Database


class RegisterFilter(BaseFilter):
    async def __call__(self, message: Message, db: Database):
        user = await db.user.get_by_user_id(user_id=message.from_user.id)
        if user is not None:
            return False

        role = await is_admin(message=message)
        if user is None:
            role = Role.USER
        await db.user.new(
            user_id=message.from_user.id,
            user_name=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language_code=message.from_user.language_code,
            role=role,
        )
        await db.session.commit()
        return True
