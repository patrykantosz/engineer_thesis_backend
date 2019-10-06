from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from food.models import Food
from enumchoicefield import ChoiceEnum, EnumChoiceField


class MealType(ChoiceEnum):
    BF = "Breakfast"
    BR = "Brunch"
    DN = "Dinner"
    LN = "Lunch"
    SU = "Supper"


class Meal(models.Model):
    food = models.ManyToManyField(Food, through='FoodDetails')
    meal_type = EnumChoiceField(enum_class=MealType, null=True)


class FoodDetails(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    food_weight = models.DecimalField(
        max_digits=6, decimal_places=3, default=100)


class UserFoodHistory(models.Model):
    meal = models.ManyToManyField(Meal)
    date = models.DateField(default=timezone.now, null=True)


class AppUser(AbstractUser):
    food_history = models.ForeignKey(
        UserFoodHistory, on_delete=models.CASCADE, null=True)
