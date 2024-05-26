from fastapi import status

from app.core.base import BaseAppError


class ProductNotFound(BaseAppError):
    """
    Product not found error
    """
    
    status_code = status.HTTP_400_BAD_REQUEST
    msg = "Product not found"
    fields = ["id"]
    

class ProductNotOwned(BaseAppError):
    """
    User is not the owner of Product
    """
    status_code = status.HTTP_403_FORBIDDEN
    msg = "User is not the owner of ingredient"
    fields = ["id"]
    

class ProductAlreadyExists(BaseAppError):
    """
    User already has product with title
    """
    status_code = status.HTTP_400_BAD_REQUEST
    fields = ["title"]
    

class IngredientsNotFound(BaseAppError):
    status_code = status.HTTP_400_BAD_REQUEST
    fields = ["ingredients"]