import asyncio

from aiogram import Bot
from aiogram.types import FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker

from src.bot.structures.keyboards import reply_keyboards as kb
from src.bot.structures.lexicon import lexicon_ru as t

from src.configuration import conf
from src.db.database import Database


async def answer_message_1(bot: Bot, user_id: int, db: Database):
    await db.user.update_state(user_id=user_id, state=1)
    await bot.send_message(
        chat_id=user_id, text=t.START_MESSAGE, reply_markup=kb.continue_mp_1
    )


async def answer_message_2(bot: Bot, user_id: int, db: Database):
    await db.user.update_state(user_id=user_id, state=2)
    await bot.send_photo(
        chat_id=user_id,
        photo=FSInputFile(conf.paths.image_path(1)),
        caption=t.MESSAGE_2,
        reply_markup=kb.continue_mp_2,
        parse_mode="HTML",
    )


async def answer_message_3(bot: Bot, user_id: int, db: Database):
    if await db.user.check_state(user_id, 2):
        await db.user.update_state(user_id=user_id, state=3)
        await bot.send_photo(
            chat_id=user_id,
            photo=FSInputFile(conf.paths.image_path(2)),
            caption=t.MESSAGE_3,
            reply_markup=kb.continue_mp_3,
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text="Нажми на кнопку",
        )


async def answer_message_4(bot: Bot, user_id: int, db: Database):
    if await db.user.check_state(user_id, 3):
        await db.user.update_state(user_id=user_id, state=4)
        await bot.send_photo(
            chat_id=user_id,
            photo=FSInputFile(conf.paths.image_path(3)),
            caption=t.MESSAGE_4,
            reply_markup=kb.continue_mp_4,
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text="Нажми на кнопку",
        )


async def answer_message_5(bot: Bot, user_id: int, db: Database):
    if await db.user.check_state(user_id, 4):
        await db.user.update_state(user_id=user_id, state=5)
        await bot.send_photo(
            chat_id=user_id,
            photo=FSInputFile(conf.paths.image_path(4)),
            caption=t.MESSAGE_5,
            reply_markup=kb.continue_mp_5,
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text="Нажми на кнопку",
        )


async def answer_message_6(bot: Bot, user_id: int, db: Database):
    if await db.user.check_state(user_id, 5):
        await db.user.update_state(user_id=user_id, state=6)
        await bot.send_photo(
            chat_id=user_id,
            photo=FSInputFile(conf.paths.image_path(5)),
            caption=t.MESSAGE_6,
            reply_markup=kb.continue_mp_6,
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text="Нажми на кнопку",
        )


async def answer_message_7(bot: Bot, user_id: int, db: Database):
    if await db.user.check_state(user_id, 6):
        await db.user.update_state(user_id=user_id, state=7)
        await bot.send_photo(
            chat_id=user_id,
            photo=FSInputFile(conf.paths.image_path(6)),
            caption=t.MESSAGE_7,
            reply_markup=kb.continue_mp_7,
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text="Нажми на кнопку",
        )


async def answer_message_8(bot: Bot, user_id: int, db: Database):
    if await db.user.check_state(user_id, 7):
        await db.user.update_state(user_id=user_id, state=8)
        await bot.send_photo(
            chat_id=user_id,
            photo=FSInputFile(conf.paths.image_path(7)),
            caption=t.MESSAGE_8,
            reply_markup=kb.continue_mp_8,
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text="Нажми на кнопку",
        )


async def spam_thread_1(bot: Bot, async_engine: AsyncEngine):
    print("start spam_thread_1")
    async_session_factory = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    while True:
        try:
            async with async_session_factory() as session:
                db = Database(session)
                users = await db.user.get_users_for_answer(delta_hours=24, count_spam=0)
                if users is None:
                    continue
                for user in users:
                    print(f"spam_thread_1: {user.user_id}")
                    await db.user.update_count_spam(user_id=user.user_id)
                    await answer_message_1(bot=bot, user_id=user.user_id, db=db)

        except Exception as e:
            print(f"error: {e}")
        await asyncio.sleep(11)


async def spam_thread_2(bot: Bot, async_engine: AsyncEngine):
    print("start spam_thread_2")
    async_session_factory = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    while True:
        try:
            async with async_session_factory() as session:
                db = Database(session)
                users = await db.user.get_users_for_answer(delta_hours=72, count_spam=1)
                if users is None:
                    continue
                for user in users:
                    print(f"spam_thread_2: {user.user_id}")
                    await db.user.update_count_spam(user_id=user.user_id)
                    await bot.send_message(
                        chat_id=user.user_id,
                        text=t.SPAM_TEXT,
                        reply_markup=kb.continue_mp_1,
                    )
                    # await answer_message_1(bot=bot, user_id=user.user_id, db=db)

        except Exception as e:
            print(f"error: {e}")
        await asyncio.sleep(12)


async def spam_thread_3(bot: Bot, async_engine: AsyncEngine):
    print("start spam_thread_3")
    async_session_factory = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    while True:
        try:
            async with async_session_factory() as session:
                db = Database(session)
                users = await db.user.get_users_for_answer(
                    delta_hours=144, count_spam=2
                )
                if users is None:
                    continue
                for user in users:
                    print(f"spam_thread_3: {user.user_id}")
                    await db.user.update_count_spam(user_id=user.user_id)
                    await bot.send_message(
                        chat_id=user.user_id,
                        text=t.SPAM_TEXT,
                        reply_markup=kb.continue_mp_1,
                    )
                    # await answer_message_1(bot=bot, user_id=user.user_id, db=db)

        except Exception as e:
            print(f"error: {e}")
        await asyncio.sleep(13)


async def spam_thread_4(bot: Bot, async_engine: AsyncEngine):
    print("start spam_thread_4")
    async_session_factory = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    while True:
        try:
            async with async_session_factory() as session:
                db = Database(session)
                users = await db.user.get_users_for_answer(
                    delta_hours=24 * 7 * 3, count_spam=3
                )
                if users is None:
                    continue
                for user in users:
                    print(f"spam_thread_4: {user.user_id}")
                    await db.user.update_count_spam(user_id=user.user_id)
                    await bot.send_message(
                        chat_id=user.user_id,
                        text=t.SPAM_TEXT,
                        reply_markup=kb.continue_mp_1,
                    )
                    # await answer_message_1(bot=bot, user_id=user.user_id, db=db)

        except Exception as e:
            print(f"error: {e}")
        await asyncio.sleep(13)
