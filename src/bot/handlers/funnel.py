from aiogram import Router, F, types
from aiogram.types import FSInputFile

from src.bot.handlers.funks import (
    answer_message_1,
    answer_message_2,
    answer_message_3,
    answer_message_4,
    answer_message_5,
    answer_message_6,
    answer_message_7,
    answer_message_8,
)
from src.bot.structures.lexicon import lexicon_ru as t
from src.configuration import conf
from src.db.database import Database

router = Router()


@router.message(F.text == t.START_MESSAGE_BTN_TEXT)
async def funnel_2(message: types.Message, db: Database):
    await answer_message_2(bot=message.bot, user_id=message.from_user.id, db=db)


@router.message(F.text == t.MESSAGE_2_BTN_TEXT)
async def funnel_3(message: types.Message, db: Database):
    await answer_message_3(bot=message.bot, user_id=message.from_user.id, db=db)


@router.message(F.text == t.MESSAGE_3_BTN_TEXT)
async def funnel_4(message: types.Message, db: Database):
    await answer_message_4(bot=message.bot, user_id=message.from_user.id, db=db)


@router.message(F.text == t.MESSAGE_4_BTN_TEXT)
async def funnel_5(message: types.Message, db: Database):
    await answer_message_5(bot=message.bot, user_id=message.from_user.id, db=db)


@router.message(F.text == t.MESSAGE_5_BTN_TEXT)
async def funnel_6(message: types.Message, db: Database):
    await answer_message_6(bot=message.bot, user_id=message.from_user.id, db=db)


@router.message(F.text == t.MESSAGE_6_BTN_TEXT)
async def funnel_7(message: types.Message, db: Database):
    await answer_message_7(bot=message.bot, user_id=message.from_user.id, db=db)


@router.message(F.text == t.MESSAGE_7_BTN_TEXT)
async def funnel_8(message: types.Message, db: Database):
    await answer_message_8(bot=message.bot, user_id=message.from_user.id, db=db)


@router.message(F.text == t.MESSAGE_8_BTN_TEXT)
async def funnel_1(message: types.Message, db: Database):
    if not await db.user.check_state(user_id=message.from_user.id, state=-1):
        await message.delete()
        await db.user.update_state(user_id=message.from_user.id, state=-1)
        await message.answer_photo(
            photo=FSInputFile(conf.paths.image_path(1)),
            caption=t.MESSAGE_2,
            parse_mode="HTML",
        )
