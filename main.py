from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import async_session, engine
from models import Base, Recipe
from schemas import RecipeCreate, RecipeOut, RecipeUpdate

app = FastAPI(
    title="Cookbook API",
    description="API для кулинарной книги с возможностью получения и создания рецептов",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()


async def get_session():
    async with async_session() as session:
        yield session


@app.get(
    "/recipes",
    response_model=List[RecipeOut],
    summary="Получить список всех рецептов",
    description="Возвращает отсортированный список рецептов: "
                "сначала по количеству просмотров (по убыванию),"
                " затем по времени приготовления (по возрастанию)",
)
async def get_recipes(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Recipe).order_by(desc(Recipe.views), asc(Recipe.cooking_time))
    )
    recipes = result.scalars().all()
    return recipes


@app.get(
    "/recipes/{recipe_id}",
    response_model=RecipeOut,
    summary="Получить детальный рецепт",
    description="Возвращает полную информацию о"
                " конкретном рецепте и увеличивает"
                " счётчик просмотров",
)
async def get_recipe(recipe_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Recipe).where(Recipe.id == recipe_id))
    recipe = result.scalar_one_or_none()
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    recipe.views += 1
    await session.commit()
    return recipe


@app.post(
    "/recipes",
    response_model=RecipeOut,
    summary="Создать новый рецепт",
    description="Добавляет новый рецепт в базу данных",
)
async def create_recipe(
    recipe: RecipeCreate, session: AsyncSession = Depends(get_session)
):
    """
    Создаёт новый рецепт в базе данных.
    """
    db_recipe = Recipe(**recipe.dict())
    session.add(db_recipe)
    await session.commit()
    await session.refresh(db_recipe)
    return db_recipe


@app.put(
    "/recipes/{recipe_id}",
    response_model=RecipeOut,
    summary="Обновить рецепт",
    description="Обновляет существующий рецепт",
)
async def update_recipe(
    recipe_id: int,
    recipe_update: RecipeUpdate,
    session: AsyncSession = Depends(get_session),
):
    """
    Обновляет существующий рецепт.
    """
    result = await session.execute(select(Recipe).where(Recipe.id == recipe_id))
    db_recipe = result.scalar_one_or_none()

    if not db_recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    for key, value in recipe_update.dict().items():
        setattr(db_recipe, key, value)

    await session.commit()
    await session.refresh(db_recipe)
    return db_recipe


@app.delete(
    "/recipes/{recipe_id}",
    summary="Удалить рецепт",
    description="Удаляет рецепт из базы данных",
)
async def delete_recipe(recipe_id: int, session: AsyncSession = Depends(get_session)):
    """
    Удаляет рецепт по ID.
    """
    result = await session.execute(select(Recipe).where(Recipe.id == recipe_id))
    db_recipe = result.scalar_one_or_none()

    if not db_recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")

    await session.delete(db_recipe)
    await session.commit()
    return {"message": "Рецепт успешно удалён"}
