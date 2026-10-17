from typing import AsyncGenerator
from core.config import settings
from core.base_model import Base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


from loguru import logger

# 创建数据库引擎和会话工厂
engine = create_async_engine(settings.database_uri, **settings.engine_options)

SessionFactory = async_sessionmaker(
    class_=AsyncSession,
    autocommit=False,
    expire_on_commit=False,
    bind=engine
)

# 数据库依赖注入
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionFactory() as session:
        try:
            yield session  # 返回数据库会话给路由处理函数
            await session.commit()  # 无异常，提交事务
        except Exception:
            await session.rollback()  #
            raise
        finally:
            await session.close()  # 关闭会话


# 用于临时使用的创建数据库表的函数
# 请在生产环境中使用 Alembic进行数据库迁移
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(lambda sys_conn: Base.metadata.create_all(sys_conn))
        logger.info("数据库表创建成功")