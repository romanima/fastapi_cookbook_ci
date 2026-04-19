import os
import sys

import pytest
from httpx import ASGITransport, AsyncClient

from .database import reset_db
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
    await reset_db()

    response = await client.post(
        "/recipes",
        json={
            "title": "Омлет",
            "cooking_time": 10,
            "ingredients": ["яйца", "молоко", "масло"],
            "description": "Классический омлет на завтрак.",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Омлет"
    assert data["views"] == 0

    recipe_id = data["id"]

    response = await client.get("/recipes")
    assert response.status_code == 200
    recipes = response.json()
    assert any(r["id"] == recipe_id for r in recipes)

    response = await client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    detail = response.json()
    assert detail["title"] == "Омлет"
    assert detail["views"] == 1

    response = await client.get(f"/recipes/{recipe_id}")
    assert response.status_code == 200
    detail = response.json()
    assert detail["views"] == 2
