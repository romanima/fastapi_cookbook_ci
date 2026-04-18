from fastapi.testclient import TestClient
from ..main import app


client = TestClient(app)

def test_get_recipes():
    response = client.get("/recipes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_recipe():
    recipe_data = {
        "title": "Тестовое блюдо",
        "cooking_time": 30,
        "ingredients": "Ингредиенты",
        "description": "Описание"
    }
    response = client.post("/recipes", json=recipe_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == recipe_data["title"]
    assert "id" in data

def test_get_recipe_by_id():
    # Сначала создаём рецепт
    recipe_data = {
        "title": "Блюдо для теста ID",
        "cooking_time": 45,
        "ingredients": "Тестовые ингредиенты",
        "description": "Тестовое описание"
    }
    create_response = client.post("/recipes", json=recipe_data)
    recipe_id = create_response.json()["id"]

    # Теперь получаем его по ID
    get_response = client.get(f"/recipes/{recipe_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == recipe_id
    assert data["title"] == recipe_data["title"]
