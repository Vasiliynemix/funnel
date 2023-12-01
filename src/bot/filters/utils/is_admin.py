from aiogram.types import Message

from src.bot.structures.role import Role
from src.configuration import conf


async def is_admin(message: Message) -> Role:
    if message.from_user.id == conf.admin.admin_id:
        return Role.ADMINISTRATOR
    return Role.USER
