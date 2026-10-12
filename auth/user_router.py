from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth.user_manager import redis_auth_backend
from auth.user_schemas import UserRead, UserCreate, UserUpdate


def register_fastapi_users_routers(
        app: FastAPI,
        fastapi_users: FastAPIUsers
):
    """把 FastAPI-User的所有router 持到app上"""
    app.include_router(
        fastapi_users.get_auth_router(redis_auth_backend),
        prefix="/auth/jwt",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_register_router(UserRead, UserCreate),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_reset_password_router(),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_verify_router(UserRead),
        prefix="/auth",
        tags=["auth"],
    )
    app.include_router(
        fastapi_users.get_users_router(UserRead, UserUpdate),
        prefix="/users",
        tags=["auth"],
    )