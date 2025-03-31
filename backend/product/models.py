import mongoengine as me
from datetime import datetime


# Create your models here.
class ProductCategory(me.Document):
    title = me.StringField(required=True, unique=True, max_length=255)
    description = me.StringField()

    meta = {"collection": "product_categories"}

    def __str__(self):
        return self.name


class Product(me.Document):
    name = me.StringField(required=True, max_length=255)
    description = me.StringField()
    category = me.ReferenceField("ProductCategory", reverse_delete_rule=me.CASCADE)
    price = me.DecimalField(required=True)
    brand = me.StringField(required=True, max_length=255)
    quantity = me.IntField(default=0, min_value=0)
    created_at = me.DateTimeField(default=datetime.utcnow)
    updated_at = me.DateTimeField(default=datetime.utcnow)

    meta = {"collection": "products"}

    def __str__(self):
        return self.name
