from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field


class DishBase(BaseModel):
    name: Annotated[str, Field(..., max_length=255, description="菜品名称")]
    description: Annotated[str | None, Field(None, description="菜品描述")]


class DishCreate(DishBase):
    pass


class DishUpdate(BaseModel):
    name: Annotated[str | None, Field(None, max_length=255, description="菜品名称")]
    description: Annotated[str | None, Field(None, description="菜品描述")]


class DishRead(DishBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
