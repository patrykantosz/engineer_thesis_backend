from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, default="")
    energy_value = models.DecimalField(max_digits=6, decimal_places=3)
    fats = models.DecimalField(max_digits=6, decimal_places=3)
    saturated_fats = models.DecimalField(
        max_digits=6, decimal_places=3, default=0)
    carbohydrates = models.DecimalField(max_digits=6, decimal_places=3)
    sugars = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    proteins = models.DecimalField(max_digits=6, decimal_places=3)
    salt = models.DecimalField(max_digits=6, decimal_places=3, default=0)
