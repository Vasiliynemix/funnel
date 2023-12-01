from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from src.bot.filters.admin import AdminFilter
from src.bot.structures.keyboards.reply_keyboards import admin_menu_mp
from src.db.database import Database

router = Router()


@router.message(Command(commands=["moderators"]), AdminFilter())
async def help_handler(
    message: Message,
    db: Database,
):
    moderators = await db.user.get_by_role()
    message_answer = ""
    for user in moderators:
        message_answer += f"{user.user_id}\n"
    await message.answer(message_answer)


@router.message(Command(commands=["admin"]), AdminFilter())
async def admin_menu_handler(message: Message):
    await message.answer("Меню Админа", reply_markup=admin_menu_mp)
