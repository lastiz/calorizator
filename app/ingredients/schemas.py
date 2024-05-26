from pydantic import BaseModel, Field


class IngredientScheme(BaseModel):
    """
    Ingredient essence scheme
    """

    id: int = Field(ge=1, description="Ingredient ID")
    title: str = Field(min_length=3, max_length=320, description="Ingredient title")
    proteins: int = Field(ge=0, description="Proteins per 100 grams")
    carbohydrates: int = Field(ge=0, description="Carbohydrates per 100 grams")
    fats: int = Field(ge=0, description="Fats per 100 grams")
    calories: int = Field(ge=0, description="Calories per 100 grams")


class AddIngredientScheme(BaseModel):
    """
    Request to add ingredient scheme
    """

    title: str = Field(min_length=3, max_length=320, description="Ingredient title")
    proteins: int = Field(ge=0, description="Proteins per 100 grams")
    carbohydrates: int = Field(ge=0, description="Carbohydrates per 100 grams")
    fats: int = Field(ge=0, description="Fats per 100 grams")
    calories: int = Field(ge=0, description="Calories per 100 grams")


class DeleteIngredientScheme(BaseModel):
    """
    Request to delete ingredient scheme
    """

    id: int


class UpdateIngredientScheme(BaseModel):
    """
    Request to update ingredient scheme
    """

    id: int = Field(ge=1, description="Ingredient ID")
    title: str | None = Field(
        min_length=3, max_length=320, description="Ingredient title"
    )
    proteins: int | None = Field(ge=0, description="Proteins per 100 grams")
    carbohydrates: int | None = Field(ge=0, description="Carbohydrates per 100 grams")
    fats: int | None = Field(ge=0, description="Fats per 100 grams")
    calories: int | None = Field(ge=0, description="Calories per 100 grams")
