from aiogram import Router, types
from aiogram.filters import CommandStart

from src.bot.filters.register import RegisterFilter
from src.bot.handlers.funks import answer_message_1
from src.bot.structures.lexicon.lexicon_ru import MESSAGE_2
from src.db.database import Database

router = Router()


@router.message(CommandStart())
@router.message(CommandStart(), RegisterFilter())
async def start_handler(message: types.Message, db: Database):
    print(message)
    if not await db.user.check_state(user_id=message.from_user.id, state=-1):
        await answer_message_1(bot=message.bot, user_id=message.from_user.id, db=db)
    else:
        await message.answer(
            f"Вы у нас уже были. Не оплатили? Вот ссылка: {MESSAGE_2[20:]}",
            reply_markup=None,
            parse_mode="HTML",
        )
