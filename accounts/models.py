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

    @staticmethod
    def get(meal_type):
        if(meal_type == "Breakfast"):
            return MealType.BF
        elif(meal_type == "Brunch"):
            return MealType.BR
        elif(meal_type == "Dinner"):
            return MealType.DN
        elif(meal_type == "Lunch"):
            return MealType.LN
        elif(meal_type == "Supper"):
            return MealType.SU
        else:
            raise Exception('InvalidValue', 'Invalid value of MealType')


class Meal(models.Model):
    food = models.ManyToManyField(Food, through='FoodDetails')
    meal_type = EnumChoiceField(enum_class=MealType, null=True)


class FoodDetails(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    food_weight = models.DecimalField(
        max_digits=6, decimal_places=3, default=100)


class UserFoodHistory(models.Model):
    meal = models.ManyToManyField(Meal, through='MealDate')


class MealDate(models.Model):
    user_food_history = models.ForeignKey(
        UserFoodHistory, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    meal_date = models.DateField(default=timezone.now, null=True)


class UserBodyParameters(models.Model):
    user_weight = models.IntegerField(default=75)
    user_height = models.IntegerField(default=180)
    user_bmi = models.DecimalField(
        max_digits=4, decimal_places=2, default=23.15)


class UserNutritionsTarget(models.Model):
    target_calories = models.IntegerField(default=1910)
    target_carbohydrates = models.IntegerField(default=270)
    target_proteins = models.IntegerField(default=50)
    target_fats = models.IntegerField(default=70)


class AppUser(AbstractUser):
    food_history = models.ForeignKey(
        UserFoodHistory, on_delete=models.CASCADE, null=True)
    body_parameters = models.ForeignKey(
        UserBodyParameters, on_delete=models.CASCADE, null=True)
    nutritions_target = models.ForeignKey(
        UserNutritionsTarget, on_delete=models.CASCADE, null=True)
