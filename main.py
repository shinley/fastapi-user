from fastapi import FastAPI

from auth.user_manager import fastapi_users
from auth.user_router import register_fastapi_users_routers
from exception.exception import register_exception_handlers
from lifespan import lifespan
from router.dish_router import router as dish_router

app = FastAPI(lifespan=lifespan, description="FastAPI-Users 练习项目实战")

# 注册全局异常处理
register_exception_handlers(app)
# 注册FastAPI-Users路由
register_fastapi_users_routers(app, fastapi_users)

@app.get("/")
async def root():
    return "hello word"

# 引入菜品路由
app.include_router(dish_router)