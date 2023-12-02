import asyncio
import logging

from aiogram import Bot
from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.bot.dispatcher import get_dispatcher, get_redis_storage
from src.bot.handlers.funks import (
    spam_thread_1,
    spam_thread_2,
    spam_thread_3,
    spam_thread_4,
)
from src.bot.structures.data_structure import TransferData
from src.configuration import conf
from src.db.database import create_async_engine, Database


async def start_bot():
    bot = Bot(token=conf.bot.token)

    async_engine = create_async_engine(url=conf.db.build_connection_str())
    async_session_factory = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session_factory() as session:
        db = Database(session)
        await db.user.delete_users()

    asyncio.create_task(spam_thread_1(bot, async_engine))
    asyncio.create_task(spam_thread_2(bot, async_engine))
    asyncio.create_task(spam_thread_3(bot, async_engine))
    asyncio.create_task(spam_thread_4(bot, async_engine))

    # await set_main_menu(bot=bot)

    # storage = get_redis_storage(
    #     redis=Redis(
    #         db=conf.redis.db,
    #         host=conf.redis.host,
    #         password=conf.redis.passwd,
    #         username=conf.redis.username,
    #         port=conf.redis.port,
    #     )
    # )

    dp = get_dispatcher()

    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        **TransferData(engine=async_engine)
    )


if __name__ == "__main__":
    logging.basicConfig(level=conf.logging_level)
    asyncio.run(start_bot())
