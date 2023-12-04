from aiogram import Router, types

from src.bot.structures.lexicon.lexicon_ru import MESSAGE_2
from src.db.database import Database

router = Router()


@router.message()
async def funnel_zero(message: types.Message, db: Database):
    if not await db.user.check_state(user_id=message.from_user.id, state=-1):
        await message.answer(text="Нажми на кнопку")
    else:
        await message.answer(
            f"Вы у нас уже были. Не оплатили? Вот ссылка: {MESSAGE_2[20:]}",
            reply_markup=None,
            parse_mode="HTML",
        )
