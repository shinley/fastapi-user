from contextlib import asynccontextmanager
from redis.asyncio import Redis

from typing import TypedDict

from fastapi import FastAPI

from core.database import create_db_and_tables

from loguru import logger

from core.redis_db import create_auth_redis


class State(TypedDict, total=False):
    auth_redis: Redis
    cache_redis: Redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- 启动 ---
    logger.info("应用启动，开始加载所有资源")

    auth_redis = create_auth_redis()
    cache_redis = create_auth_redis()
    logger.info("Redis 已就绪")

    # 运行
    yield State(auth_redis=auth_redis, cache_redis=cache_redis)
    # --- 关闭时执行 ---
    await cache_redis.aclose()
    await auth_redis.aclose()

    logger.info("应用关闭, 资源已释放")