from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTableUUID
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from core.base_model import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    name: Mapped[str] = mapped_column(String(64), nullable=False)


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass