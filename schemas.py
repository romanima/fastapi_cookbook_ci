from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RecipeBase(BaseModel):
    title: str
    cooking_time: int
    ingredients: str
    description: str


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(RecipeBase):
    pass


class RecipeOut(RecipeBase):
    id: int
    views: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        json_encoders = {datetime: lambda v: v.isoformat()}
