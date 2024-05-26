from pydantic import BaseModel, Field

from app.ingredients.schemas import IngredientScheme


class ProductIngredientScheme(BaseModel):
    """
    Product ingredient relation scheme
    """
    ingredient_id: int = Field(ge=1, description="Ingredient ID")
    grams: int = Field(ge=0, description="Ingredient amount of grams")


class ProductScheme(BaseModel):
    """
    Product essence scheme
    """
    id: int = Field(ge=1, description="Product ID")
    title: str = Field(min_length=3, max_length=320, description="Product Title")
    ingredients: list[ProductIngredientScheme] = Field(min_length=1, description="Product ingredients in grams")


class ProductWithIngredientsScheme(BaseModel):
    id: int = Field(ge=1, description="Product ID")
    title: str = Field(min_length=3, max_length=320, description="Product Title")
    # ingredients: list[ProductIngredientScheme] = Field(description="Product ingredients")


class AddProductScheme(BaseModel):
    """
    Request to add product scheme
    """
    title: str = Field(min_length=3, max_length=320, description="Product Title")
    ingredients: list[ProductIngredientScheme] = Field(min_length=1, description="Product ingredients")


class DeleteProductScheme(BaseModel):
    """
    Request to delete product scheme
    """
    product_id: int = Field(ge=1, description="Product ID")
    

class UpdateProductScheme(BaseModel):
    """
    Request to update product scheme
    """
    id: int = Field(ge=1, description="Product ID")
    title: str | None = Field(min_length=3, max_length=320, description="Product title")
    ingredients: list[ProductIngredientScheme] | None = Field(min_length=1, description="Product ingredients")
    