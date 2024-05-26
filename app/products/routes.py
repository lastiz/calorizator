from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.products.schemas import (
    ProductScheme,
    AddProductScheme,
    DeleteProductScheme,
    UpdateProductScheme,
)
from app.auth.dependencies import get_current_user, User
from app.products.dependencies import get_product_service, ProductService


router = APIRouter(prefix="/products", tags=["Products operations"])


@router.get("", response_model=list[ProductScheme])
async def get_products(
    user: Annotated[User, Depends(get_current_user)],
    product_service: Annotated[ProductService, Depends(get_product_service)],
    product_title: Annotated[
        str | None, Query(max_length=320, description="Product title")
    ] = None,
):
    """
    Get user products with title like %product_title%
    """
    return await product_service.get(user, product_title)


@router.post("", response_model=ProductScheme, status_code=201)
async def create_product(
    user: Annotated[User, Depends(get_current_user)],
    product_service: Annotated[ProductService, Depends(get_product_service)],
    scheme: AddProductScheme,
):
    """
    Create user product
    """
    return await product_service.create(user, scheme.title, scheme.ingredients)


@router.delete("", response_model=int)
async def delete_product(
    user: Annotated[User, Depends(get_current_user)],
    product_service: Annotated[ProductService, Depends(get_product_service)],
    scheme: DeleteProductScheme,
):
    """
    Delete user product
    """
    return await product_service.delete(user, scheme.product_id)


@router.put("", response_model=ProductScheme)
async def update_product(
    user: Annotated[User, Depends(get_current_user)],
    product_service: Annotated[ProductService, Depends(get_product_service)],
    scheme: UpdateProductScheme,
):
    """
    Update user product
    """
    return await product_service.update(user, scheme)
