import mongoengine as me

# Create your models here.
class Product(me.Document):
    name = me.StringField(required=True, max_length = 255)
    description = me.StringField()
    category = me.StringField(required=True, max_length = 255)
    price = me.DecimalField(required=True)
    brand = me.StringField(required=True, max_length = 255)
    quantity = me.IntField(default = 0, min_value=0)

    meta = {'collection': 'products'}

    def __str__(self):
        return self.name