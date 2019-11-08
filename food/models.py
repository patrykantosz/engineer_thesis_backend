from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, default="")
    energy_value = models.IntegerField()
    fats = models.DecimalField(max_digits=6, decimal_places=1)
    saturated_fats = models.DecimalField(
        max_digits=6, decimal_places=1)
    carbohydrates = models.DecimalField(max_digits=6, decimal_places=1)
    sugars = models.DecimalField(max_digits=6, decimal_places=1)
    proteins = models.DecimalField(max_digits=6, decimal_places=1)
    salt = models.DecimalField(max_digits=7, decimal_places=2)
