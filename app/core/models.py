from tortoise.fields import OnDelete
from tortoise.models import Model
from tortoise import fields

from app.core.model_mixins import TimeMixin


### USERS AND AUTHORIZATION ###

class User(Model, TimeMixin):
    """
    Represents User essence
    """
    id = fields.IntField(primary_key=True)
    
    # creds
    username = fields.CharField(max_length=32, indexable=True, unique=True)
    email = fields.CharField(max_length=320, unique=True)
    hashed_password = fields.CharField(max_length=516)
    token = fields.CharField(max_length=516, indexable=True, null=True, blank=True, unique=True)
    
    is_admin = fields.BooleanField(default=False)
    online_at = fields.DatetimeField(auto_now=True)
    
    class Meta:
        table = "users"


class Ingredient(Model, TimeMixin):
    """
    Represents Ingredient essence with nutrients per 100 grams
    """
    id = fields.IntField(primary_key=True)
    
    title = fields.CharField(max_length=320, indexable=True)
    proteins = fields.IntField(default=0)
    carbohydrates = fields.IntField(default=0)
    fats = fields.IntField(default=0)
    calories = fields.IntField(default=0)
    
    owner = fields.ForeignKeyField("models.User", related_name="ingredients", on_delete=OnDelete.CASCADE)
    # products = fields.ManyToManyField("models.Product", through="product_ingredient")
    
    class Meta:
        table = "ingredients"
    

class Product(Model, TimeMixin):
    """
    Represents Product essence
    """
    id = fields.IntField(primary_key=True)
    
    title = fields.CharField(max_length=320)
    
    owner = fields.ForeignKeyField("models.User", related_name="products", on_delete=OnDelete.CASCADE)
    # ingredients = fields.ManyToManyField("models.Ingredient", through="product_ingredient")

    class Meta:
        table = "products"
        

class ProductIngredient(Model):
    """
    Represents product ingredient in grams
    """
    id = fields.IntField(primary_key=True)
    
    product = fields.ForeignKeyField("models.Product", on_delete=OnDelete.CASCADE, related_name="ingredients")
    ingredient = fields.ForeignKeyField("models.Ingredient", on_delete=OnDelete.CASCADE, related_name="products")
    grams = fields.IntField()
    
    class Meta:
        table = "product_ingredient"
    