from sqlalchemy import asc, desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Recipe
from schemas import RecipeCreate


async def get_recipes(session: AsyncSession):
    result = await session.execute(
        select(Recipe).order_by(desc(Recipe.views), asc(Recipe.cooking_time))
    )
    recipes = result.scalars().all()
    return recipes


async def get_recipe_details(session: AsyncSession, recipe_id: int):
    recipe = await session.get(Recipe, recipe_id)
    if recipe:
        recipe.views += 1
        await session.commit()
        await session.refresh(recipe)
        recipe_dict = {
            "id": recipe.id,
            "title": recipe.title,
            "cooking_time": recipe.cooking_time,
            "ingredients": [
                i.strip() for i in recipe.ingredients.split(",") if i.strip()
            ],
            "description": recipe.description,
            "views": recipe.views,
        }
        return recipe_dict
    return None


async def create_recipe(session: AsyncSession, recipe_in: RecipeCreate):
    recipe = Recipe(
        title=recipe_in.title,
        cooking_time=recipe_in.cooking_time,
        ingredients=", ".join(recipe_in.ingredients),
        description=recipe_in.description,
        views=0,
    )
    session.add(recipe)
    await session.commit()
    await session.refresh(recipe)
    return {
        "id": recipe.id,
        "title": recipe.title,
        "cooking_time": recipe.cooking_time,
        "ingredients": [i.strip() for i in recipe.ingredients.split(",") if i.strip()],
        "description": recipe.description,
        "views": recipe.views,
    }
