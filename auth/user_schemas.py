import datetime
import uuid

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[uuid.UUID]):
    name: str | None = Field(None, max_length=64)
    created_at: datetime.datetime | None = Field(None)
    updated_at: datetime.datetime | None = Field(None)


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    name: str | None = Field(None, max_length=64)