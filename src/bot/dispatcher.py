from aiogram import Dispatcher
from aiogram.fsm.storage.base import BaseEventIsolation, BaseStorage
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.strategy import FSMStrategy
from redis.asyncio.client import Redis

from src.bot.handlers import routers
from src.bot.middlewares.middleware_db import DatabaseMiddleware
from src.configuration import conf


def get_redis_storage(
    redis: Redis, state_ttl=conf.redis.state_ttl, data_ttl=conf.redis.data_ttl
):
    return RedisStorage(redis=redis, state_ttl=state_ttl, data_ttl=data_ttl)


def get_dispatcher(
    storage: BaseStorage | None = None,
    fsm_strategy: FSMStrategy | None = FSMStrategy.CHAT,
    event_isolation: BaseEventIsolation | None = None,
):
    dp = Dispatcher(
        storage=storage or MemoryStorage(),
        fsm_strategy=fsm_strategy,
        events_isolation=event_isolation,
    )

    for router in routers:
        dp.include_router(router)

    # Register middlewares
    dp.message.outer_middleware(DatabaseMiddleware())
    dp.callback_query.outer_middleware(DatabaseMiddleware())

    return dp
