from django.db import models
from django.contrib.auth.models import User
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
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    meal_type = EnumChoiceField(enum_class=MealType, null=True)


class UserFoodHistory(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=timezone.now(), null=True)


class AppUser(User):
    food_history = models.ForeignKey(
        UserFoodHistory, on_delete=models.CASCADE, null=True)
