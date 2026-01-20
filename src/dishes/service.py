from typing import Mapping, Any

from sqlalchemy.exc import IntegrityError

from src.dishes.model import Dish
from src.dishes.repository import DishRepository
from src.dishes.schema import DishCreate, DishUpdate


class DishService:
    def __init__(self, repository: DishRepository):
        self.repository = repository

    async def create_dish(self, dish_data: DishCreate) -> Dish:
        try:
            dish = await self.repository.create(dish_data.model_dump())
            return dish
        except IntegrityError as e:
            raise ValueError("菜品名称已存在") from e

    async def get_dish(self, dish_id: int) -> Dish | None:
        return await self.repository.get_by_id(dish_id)

    async def list_dishes(
        self,
        search: str | None = None,
        order_by: str = "id",
        direction: str = "asc",
        limit: int = 10,
        offset: int = 0,
    ) -> list[Dish]:
        return await self.repository.get_all(
            search=search,
            order_by=order_by,
            direction=direction,
            limit=limit,
            offset=offset,
        )

    async def update_dish(self, dish_id: int, dish_data: DishUpdate) -> Dish | None:
        update_data = dish_data.model_dump(exclude_unset=True)
        if not update_data:
            return await self.repository.get_by_id(dish_id)
        return await self.repository.update(update_data, dish_id)

    async def delete_dish(self, dish_id: int) -> bool:
        return await self.repository.delete(dish_id)
