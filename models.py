from sqlalchemy import Column, Integer, String, Text

from base import Base


class Recipe(Base):
    """
    Модель рецепта.
    """

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False, index=True, doc="Название рецепта")
    cooking_time = Column(Integer, nullable=False, doc="Время готовки (минуты)")
    ingredients = Column(Text, nullable=False, doc="Ингредиенты через запятую")
    description = Column(Text, nullable=False, doc="Текстовое описание рецепта")
    views = Column(Integer, default=0, nullable=False, doc="Количество просмотров")

    def __repr__(self):
        return f"<Recipe(id={self.id}, title='{self.title}')>"
