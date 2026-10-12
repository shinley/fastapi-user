from sqlalchemy import MetaData, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.config import settings

from datetime import datetime, timezone

database_naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

class Base(DeclarativeBase):
    # 全局统一metadata
    metadata = MetaData(naming_convention=database_naming_convention)


class DateTimeMixin:
    if settings.db_type == "postgres":
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
            index=True
        )
        updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=func.now(),
            nullable=False,
            onupdate=func.now(),
        )
    else:
        # SQLite 使用Python 层默认值判模拟
        created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=datetime.now(timezone.utc),
            nullable=False,
            index=True
        )
        updated_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True),
            server_default=datetime.now(timezone.utc),
            nullable=False,
            onupdate=datetime.now(timezone.utc),
        )
