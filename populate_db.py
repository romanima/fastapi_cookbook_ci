import asyncio

from main import Recipe, get_session

# Тестовые данные
recipes_data = [
    {
        "title": "Борщ",
        "cooking_time": 120,
        "ingredients": "Свёкла — 1 шт.,"
                       " Картофель — 3 шт., Капуста — 200 г,"
                       " Морковь — 1 шт., Лук — 1 шт., Мясо — 300 г",
        "description": "Сварить бульон. "
                       "Обжарить овощи. Добавить в бульон, варить 1,5 часа.",
    },
    {
        "title": "Пицца Маргарита",
        "cooking_time": 30,
        "ingredients": "Тесто для пиццы — 200 г,"
                       " Томатный соус — 3 ст. л., Моцарелла — 100 г,"
                       " Базилик — несколько листиков",
        "description": "Раскатать тесто."
                       " Смазать соусом, выложить сыр."
                       " Выпекать 15 минут при 220°C.",
    },
]


async def populate_database():
    async for session in get_session():
        for recipe_data in recipes_data:
            recipe = Recipe(**recipe_data)
            session.add(recipe)
        await session.commit()
        print("База данных наполнена тестовыми рецептами!")


if __name__ == "__main__":
    asyncio.run(populate_database())
