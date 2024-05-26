from tortoise import fields


class TimeMixin:
    """
    Миксин добавляет общие поля времени к моделям
    """

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
