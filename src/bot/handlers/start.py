from aiogram import Router, types
from aiogram.filters import CommandStart

from src.bot.filters.register import RegisterFilter
from src.bot.handlers.funks import answer_message_1
from src.db.database import Database

router = Router()


@router.message(CommandStart())
@router.message(CommandStart(), RegisterFilter())
async def start_handler(message: types.Message, db: Database):
    await answer_message_1(bot=message.bot, user_id=message.from_user.id, db=db)
