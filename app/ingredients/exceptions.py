from fastapi import status

from app.core.base import BaseAppError


class IngredientNotFound(BaseAppError):
    """
    Ingredient not found error
    """

    status_code = status.HTTP_400_BAD_REQUEST
    msg = "Ingredient not found"
    fields = ["id"]


class IngredientNotOwned(BaseAppError):
    """
    User is not the owner of ingredient
    """

    status_code = status.HTTP_403_FORBIDDEN
    msg = "User is not the owner of ingredient"
    fields = ["id"]


class IngredientAlreadyExists(BaseAppError):
    """
    User already has ingredient with title
    """

    status_code = status.HTTP_400_BAD_REQUEST
    fields = ["title"]
