from tortoise.transactions import atomic

from app.core.models import Ingredient, User, Product, ProductIngredient
from app.products.exceptions import (
    ProductAlreadyExists,
    ProductNotOwned,
    ProductNotFound,
    IngredientsNotFound,
)
from app.products.schemas import ProductIngredientScheme, UpdateProductScheme


class ProductService:
    """
    Business logic for product domain
    """

    async def get(self, user: User, title: str | None) -> list[Product]:
        """
        Returns user products with title like %:title%
        """
        query = Product.filter(owner=user).prefetch_related("ingredients")
        if title:
            query = query.filter(title__icontains=title)

        return await query.order_by("title")

    @atomic()
    async def create(
        self, user: User, title: str, prod_ingreds: list[ProductIngredientScheme]
    ) -> Product:
        """
        Creates and returns created product
        """
        if await self.product_exists(user, title):
            raise ProductAlreadyExists(
                msg=f"User already has product with title [{title}]"
            )

        if not await self.check_ingredients_existence(user, prod_ingreds):
            raise IngredientsNotFound(f"Invalid ingredient ids")

        product = await Product.create(owner=user, title=title)
        await self.create_product_ingredients(product, prod_ingreds)
        await product.save()
        await product.fetch_related("ingredients")
        return product

    async def delete(self, user: User, product_id: int) -> int:
        """
        Deletes and returns deleted user product
        """
        product = await Product.get_or_none(id=product_id)

        if not product:
            raise ProductNotFound()

        if product.owner_id != user.id:  # type: ignore
            raise ProductNotOwned()

        await product.delete()
        return product.id

    @atomic()
    async def update(self, user: User, data_scheme: UpdateProductScheme):
        """
        Updates user product
        """
        product = await Product.get_or_none(id=data_scheme.id).prefetch_related(
            "ingredients"
        )

        if product is None:
            raise ProductNotFound()

        if product.owner_id != user.id:  # type: ignore
            raise ProductNotOwned()

        updated_ingreds = data_scheme.ingredients
        updated_title = data_scheme.title

        if (
            updated_title is not None
            and product.title != updated_title
            and await self.product_exists(user, updated_title)
        ):
            raise ProductAlreadyExists(
                msg=f"User already has product with title [{updated_title}]"
            )

        if updated_title is not None:
            product.title = updated_title
            await product.save(update_fields=["title"])

        if updated_ingreds is not None:
            if not await self.check_ingredients_existence(user, updated_ingreds):
                raise IngredientsNotFound(f"Invalid ingredient ids")

            await self.update_product_ingredients(product, updated_ingreds)
            await product.fetch_related("ingredients")

        return product

    async def product_exists(self, user: User, title: str) -> bool:
        return await Product.exists(owner=user, title=title)

    async def create_product_ingredients(
        self, product: Product, prod_ingreds: list[ProductIngredientScheme]
    ) -> list[ProductIngredient]:
        """
        Creates list of product ingredients instances
        """
        instances = []
        for pi in prod_ingreds:
            instance = ProductIngredient(
                product_id=product.id, ingredient_id=pi.ingredient_id, grams=pi.grams
            )
            instances.append(instance)

        await ProductIngredient.bulk_create(instances)
        return instances

    async def update_product_ingredients(
        self, product: Product, prod_ingreds: list[ProductIngredientScheme]
    ) -> list[ProductIngredient]:
        """
        Updates product ingredient instances
        """
        instances = []
        for pi in prod_ingreds:
            instance = ProductIngredient(
                product_id=product.id, ingredient_id=pi.ingredient_id, grams=pi.grams
            )
            instances.append(instance)

        await ProductIngredient.bulk_create(
            instances,
            on_conflict=["product_id", "ingredient_id"],
            update_fields=["grams"],
        )
        await ProductIngredient.filter(product=product).exclude(
            ingredient_id__in=[pi.ingredient_id for pi in prod_ingreds]
        ).delete()
        return instances

    async def check_ingredients_existence(
        self, user: User, prod_ingreds: list[ProductIngredientScheme]
    ):
        """
        Checks if user has all ingredients in prod_ingreds
        """
        ingredients_ids = [pi.ingredient_id for pi in prod_ingreds]
        ingredients_count = await Ingredient.filter(
            owner=user,
            id__in=ingredients_ids,
        ).count()
        return ingredients_count == len(ingredients_ids)
