# src/dishes/router.py
from typing import Literal

from fastapi import APIRouter, Depends, Path, Query, status
from loguru import logger
from core.database import get_db
from repository.dish_repository import DishRepository
from schemas.dish_schema import DishCreate, DishResponse, DishUpdate
from service.dish_service import DishService

from auth.user_manager import get_current_user, current_superuser

router = APIRouter(
    prefix="/dishes", tags=["Dishes"], dependencies=[Depends(get_current_user)],
)


"""
✅ 每次请求都会调用 get_dish_service，并新建 DishRepository 和 DishService。

✅ 同一请求内多次依赖同一个 get_dish_service 只会执行一次（默认缓存）。

✅ 这是正常且推荐的做法，因为 Session 是请求级的。

⚠️ 不要随意用 @lru_cache 缓存这个依赖，否则会导致 Session 跨请求复用，引发并发问题。

🚀 性能瓶颈通常不在这些对象的实例化，而在数据库查询、连接池配置和异步 I/O。

所以你的写法没有问题，保持现状即可。
"""
# 注入仓库 + 服务层
async def get_dish_service(session=Depends(get_db)) -> DishService:
    repository = DishRepository(session)
    return DishService(repository)


@router.post("/", response_model=DishResponse, status_code=status.HTTP_201_CREATED)
async def create_dish(
    dish_data: DishCreate, service: DishService = Depends(get_dish_service)
):
    """创建菜品"""
    new_dish = await service.create_dish(dish_data)
    return new_dish


@router.get("/{dish_id}", response_model=DishResponse)
async def get_dish(
    dish_id: int = Path(..., description="菜品ID"),
    service: DishService = Depends(get_dish_service),
):
    """获取单个菜品"""

    logger.debug(f"正在获取菜品 ID: {dish_id}")
    try:
        dish = await service.get_dish_by_id(dish_id)
        logger.info(f"获取到菜品, ID: {dish_id}")
        return dish
    except Exception as e:
        logger.error(f"获取 ID 为 {dish_id} 的菜品时出错: {e!s}")
        raise


@router.get("/", response_model=list[DishResponse])
async def list_dishes(
    search: str | None = Query(None, description="搜索关键词"),
    order_by: Literal["id", "name", "created_at"] = Query("id", description="排序字段"),
    direction: Literal["asc", "desc"] = Query("asc", description="排序方向"),
    limit: int = Query(10, ge=1, le=500),
    offset: int = Query(0, ge=0),
    service: DishService = Depends(get_dish_service),
):
    """查询所有菜品"""
    dishes = await service.list_dishes(
        search=search,
        order_by=order_by,
        direction=direction,
        limit=limit,
        offset=offset,
    )
    return dishes


@router.patch("/{dish_id}", response_model=DishResponse)
async def update_dish(
    dish_data: DishUpdate,
    dish_id: int = Path(..., description="菜品ID"),
    service: DishService = Depends(get_dish_service),
):
    """更新菜品"""
    dish = await service.update_dish(dish_id, dish_data)
    return dish

# superuser 才能删除
@router.delete(
    "/{dish_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(current_superuser)],
)
async def delete_dish(
    dish_id: int = Path(..., description="菜品ID"),
    service: DishService = Depends(get_dish_service),
):
    """删除菜品"""

    await service.delete_dish(dish_id)