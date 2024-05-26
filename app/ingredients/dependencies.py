from app.ingredients.service import IngredientService


def get_ingredients_service() -> IngredientService:
    return IngredientService()