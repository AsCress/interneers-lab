import mongoengine as me
from datetime import datetime


# Create your models here.
class ProductCategory(me.Document):
    title = me.StringField(required=True, unique=True, max_length=255)
    description = me.StringField(default="")

    meta = {"collection": "product_categories"}

    def __str__(self):
        return self.title


class Product(me.Document):
    name = me.StringField(required=True, max_length=255)
    description = me.StringField()
    category = me.ReferenceField(
        "ProductCategory", reverse_delete_rule=me.CASCADE, required=True
    )
    price = me.DecimalField(required=True, min_value=0)
    brand = me.StringField(required=True, max_length=255)
    quantity = me.IntField(required=True, default=0, min_value=0)
    created_at = me.DateTimeField(default=datetime.utcnow)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {"collection": "products"}

    def __str__(self):
        return self.name
