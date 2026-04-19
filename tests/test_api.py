import os
import sys

import pytest
from httpx import ASGITransport, AsyncClient

from database import reset_db
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
    # 1. Сбрасываем БД — удаляем и создаём все таблицы
    await reset_db(engine)
    
    # 2. Даём время на завершение операций
    await asyncio.sleep(0.1)
    
    # 3. Отправляем запрос к API
    response = await client.post(
        "/recipes",
        json={
            "title": "Омлет",
            "cooking_time": 10,
            "ingredients": ["яйца", "молоко", "масло"],
            "description": "Классический омлет на завтрак.",
        },
    )
    
    # 4. Проверяем результат
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Омлет"
    assert data["cooking_time"] == 10
