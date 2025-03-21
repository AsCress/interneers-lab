from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length = 255)
    description = models.TextField(blank = True, null = True)
    category = models.CharField(max_length = 255)
    price = models.DecimalField(max_digits = 10, decimal_places = 2)
    brand = models.CharField(max_length = 255)
    quantity = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.name