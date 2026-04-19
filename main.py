from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import crud
from database import get_async_session, init_db
from schemas import RecipeCreate, RecipeDetails, RecipeList


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управление жизненным циклом приложения.

    Выполняет инициализацию базы данных перед запуском сервиса.
    Позволяет впоследствии добавить очистку ресурсов при остановке.
    Вместо deprecated
    @app.on_event("startup")
    async def on_startup():
        await init_db()
    """
    await init_db()
    yield
    # Возможная логика для остановки и очистки ресурсов здесь


app = FastAPI(
    title="Кулинарная книга API",
    description="Асинхронный бэкенд-сервис" " для хранения и предоставления рецептов.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/recipes", response_model=List[RecipeList])
async def get_recipes(session: AsyncSession = Depends(get_async_session)):
    """
    Получить список всех рецептов с сортировкой по
    популярности и времени готовки.

    - Возвращает отсортированный список рецептов.
    """
    return await crud.get_recipes(session)


@app.get("/recipes/{recipe_id}", response_model=RecipeDetails)
async def get_recipe(
    recipe_id: int, session: AsyncSession = Depends(get_async_session)
):
    """
    Получить детальную информацию о рецепте по идентификатору.

    - Увеличивает количество просмотров рецепта при каждом запросе.
    - Возвращает подробную информацию:
    название, время готовки, ингредиенты, описание, количество просмотров.
    - В случае отсутствия рецепта возвращает 404 ошибку.
    """
    recipe = await crud.get_recipe_details(session, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return recipe


@app.post("/recipes", response_model=RecipeDetails, status_code=201)
async def create_recipe(
    recipe: RecipeCreate, session: AsyncSession = Depends(get_async_session)
):
    """
    Создать новый рецепт.

    - Принимает данные рецепта.
    - Возвращает созданный рецепт с полным описанием.
    """
    return await crud.create_recipe(session, recipe)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
