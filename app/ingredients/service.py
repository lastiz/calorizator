from app.core.models import Ingredient, User
from app.ingredients.exceptions import (
    IngredientNotFound,
    IngredientNotOwned,
    IngredientAlreadyExists,
)
from app.ingredients.schemas import UpdateIngredientScheme


class IngredientService:
    """
    Business logic for ingredient domain
    """

    async def get(self, user: User, title: str | None) -> list[Ingredient]:
        """
        Returns user ingredients with title like %:title%
        """
        query = Ingredient.filter(owner=user)
        if title:
            query = query.filter(title__icontains=title)

        return await query.order_by("title")

    async def create(
        self,
        user: User,
        title: str,
        proteins: int,
        carbohydrates: int,
        fats: int,
        calories: int,
    ) -> Ingredient:
        """
        Creates and returns ingredient
        """
        if await self.ingredient_exists(user, title):
            raise IngredientAlreadyExists(
                msg=f"User already has ingredient with title [{title}]"
            )

        ingredient = await Ingredient.create(
            owner=user,
            title=title,
            proteins=proteins,
            carbohydrates=carbohydrates,
            fats=fats,
            calories=calories,
        )
        return ingredient

    async def delete(self, user: User, ingredient_id: int) -> int:
        """
        Deletes user ingredient
        """
        ingredient = await Ingredient.get_or_none(id=ingredient_id)

        if not ingredient:
            raise IngredientNotFound()

        if ingredient.owner_id != user.id:  # type: ignore
            raise IngredientNotOwned()

        await ingredient.delete()
        return ingredient.id

    async def update(
        self,
        user: User,
        data_scheme: UpdateIngredientScheme,
    ):
        """
        Edits user ingredient
        """
        ingredient = await Ingredient.get_or_none(id=data_scheme.id)

        if ingredient is None:
            raise IngredientNotFound()

        if ingredient.owner_id != user.id:  # type: ignore
            raise IngredientNotOwned()

        updated_data = data_scheme.model_dump(exclude={"id"}, exclude_none=True)
        updated_title = data_scheme.title

        if (
            updated_title is not None
            and ingredient.title != updated_title
            and await self.ingredient_exists(user, updated_title)
        ):
            raise IngredientAlreadyExists(
                msg=f"User already has ingredient with title [{updated_title}]"
            )

        ingredient = await ingredient.update_from_dict(
            data_scheme.model_dump(exclude={"ingredient_id"}, exclude_none=True)
        )
        await ingredient.save(update_fields=updated_data)
        return ingredient

    async def ingredient_exists(self, user: User, title: str):
        return await Ingredient.exists(owner=user, title=title)
