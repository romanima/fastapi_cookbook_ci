from typing import List

from pydantic import BaseModel, Field, constr


class RecipeList(BaseModel):
    """Краткая информация о рецепте (для списка)."""

    id: int
    title: constr(max_length=255)
    cooking_time: int = Field(..., description="Время готовки в минутах")
    views: int = Field(..., description="Количество просмотров")

    model_config = {"from_attributes": True}


class RecipeCreate(BaseModel):
    """Схема запроса создания рецепта."""

    title: constr(max_length=255)
    cooking_time: int = Field(..., gt=0, description="Время готовки в " "минутах (>0)")
    ingredients: List[constr(strip_whitespace=True, min_length=1)]
    description: str


class RecipeDetails(BaseModel):
    """Полная информация о рецепте (детально)."""

    id: int
    title: constr(max_length=255)
    cooking_time: int
    ingredients: List[str]
    description: str
    views: int

    model_config = {"from_attributes": True}
