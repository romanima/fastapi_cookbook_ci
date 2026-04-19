import os
import sys
import pytest
import asyncio
import pytest
from sqlalchemy import inspect
from httpx import ASGITransport, AsyncClient

from database import reset_db, engine
from main import app

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        yield ac


@pytest.mark.asyncio
async def test_recipes_crud(client):
    # 1. Сбрасываем БД
    await reset_db(engine)

    # 2. Ждём завершения операций
    await asyncio.sleep(0.1)

    # 3. Проверяем, что таблица recipes создана
    async with engine.connect() as conn:
        inspector = inspect(conn)
        tables = await conn.run_sync(inspector.get_table_names)
        assert "recipes" in tables, "Таблица recipes не создана после reset_db"

    # 4. Отправляем запрос к API
    response = await client.post(
        "/recipes",
        json={
            "title": "Омлет",
            "cooking_time": 10,
            "ingredients": ["яйца", "молоко", "масло"],
            "description": "Классический омлет на завтрак.",
        },
    )

    # 5. Проверяем результат
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Омлет"
    assert data["cooking_time"] == 10
