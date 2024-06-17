from typing import Annotated
from fastapi import APIRouter, Depends, Query

from app.ingredients.schemas import (
    IngredientScheme,
    AddIngredientScheme,
    DeleteIngredientScheme,
    UpdateIngredientScheme,
)
from app.auth.dependencies import get_current_user, User
from app.ingredients.dependencies import get_ingredients_service, IngredientService


router = APIRouter(prefix="/ingredients", tags=["Ingredients operations"])


@router.get("", response_model=list[IngredientScheme])
async def get_ingredients(
    user: Annotated[User, Depends(get_current_user)],
    ingredient_service: Annotated[IngredientService, Depends(get_ingredients_service)],
    ingredient_title: Annotated[
        str | None, Query(max_length=320, description="Ingredient title")
    ] = None,
):
    """
    Get user ingredients with title like %ingredient_title%
    """
    return await ingredient_service.get(user, ingredient_title)


@router.post("", response_model=IngredientScheme, status_code=201)
async def create_ingredients(
    user: Annotated[User, Depends(get_current_user)],
    ingredient_service: Annotated[IngredientService, Depends(get_ingredients_service)],
    scheme: AddIngredientScheme,
):
    """
    Create user ingredient
    """
    return await ingredient_service.create(user, **scheme.model_dump())


@router.delete("", response_model=DeleteIngredientScheme)
async def delete_ingredient(
    user: Annotated[User, Depends(get_current_user)],
    ingredient_service: Annotated[IngredientService, Depends(get_ingredients_service)],
    scheme: DeleteIngredientScheme,
):
    """
    Delete user ingredient
    """
    return await ingredient_service.delete(user, scheme.id)


@router.put("", response_model=IngredientScheme)
async def update_ingredient(
    user: Annotated[User, Depends(get_current_user)],
    ingredient_service: Annotated[IngredientService, Depends(get_ingredients_service)],
    scheme: UpdateIngredientScheme,
):
    """
    Update user ingredient
    """
    return await ingredient_service.update(user, scheme)
