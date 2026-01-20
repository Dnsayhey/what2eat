from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from src.core.database import get_db
from src.dishes.model import Dish
from src.dishes.repository import DishRepository
from src.dishes.schema import DishCreate, DishRead, DishUpdate
from src.dishes.service import DishService
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/dishes", tags=["dishes"])


def get_dish_service(session: AsyncSession = Depends(get_db)) -> DishService:
    repository = DishRepository(session)
    return DishService(repository)


@router.post("", response_model=DishRead, status_code=status.HTTP_201_CREATED)
async def create_dish(
    dish_data: DishCreate,
    service: DishService = Depends(get_dish_service),
) -> Dish:
    try:
        return await service.create_dish(dish_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        ) from e


@router.get("/{dish_id}", response_model=DishRead)
async def get_dish(
    dish_id: int,
    service: DishService = Depends(get_dish_service),
) -> Dish:
    dish = await service.get_dish(dish_id)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="菜品不存在",
        )
    return dish


@router.get("", response_model=List[DishRead])
async def list_dishes(
    search: str | None = None,
    order_by: str = "id",
    direction: str = "asc",
    limit: int = 10,
    offset: int = 0,
    service: DishService = Depends(get_dish_service),
) -> List[Dish]:
    return await service.list_dishes(
        search=search,
        order_by=order_by,
        direction=direction,
        limit=limit,
        offset=offset,
    )


@router.put("/{dish_id}", response_model=DishRead)
async def update_dish(
    dish_id: int,
    dish_data: DishUpdate,
    service: DishService = Depends(get_dish_service),
) -> Dish:
    dish = await service.update_dish(dish_id, dish_data)
    if not dish:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="菜品不存在",
        )
    return dish


@router.delete("/{dish_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dish(
    dish_id: int,
    service: DishService = Depends(get_dish_service),
) -> None:
    success = await service.delete_dish(dish_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="菜品不存在",
        )
