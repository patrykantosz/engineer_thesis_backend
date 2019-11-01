from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AppUser, UserFoodHistory, Meal, FoodDetails, MealDate
from food.serializer import FoodSerializer
from django.core import serializers as coreserializers
from food.models import Food
from django.db.models.query import QuerySet


class FoodDetailsSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if type(self.root.instance) == QuerySet:
            self.root.instance = self.root.instance[0]
        food_details = FoodDetails.objects.filter(
            food=value, meal=self.root.instance).first()
        food_weight = food_details.food_weight
        value = FoodSerializer(value)
        serialized_food_data = value.data
        serialized_food_data['food_details_id'] = str(food_details.id)
        serialized_food_data['food_weight'] = str(food_weight)

        return serialized_food_data


class MealSerializer(serializers.ModelSerializer):
    food = FoodDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = ('id', 'meal_type', 'food')


class MealDateSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if type(self.root.instance) == QuerySet:
            self.root.instance = self.root.instance[0]
        meal_date_object = MealDate.objects.filter(
            meal=value, user_food_history=self.root.instance).first()
        meal_date = meal_date_object.meal_date
        value = MealSerializer(value)
        serialized_meal_data = value.data
        serialized_meal_data['meal_date_id'] = str(meal_date_object.id)
        serialized_meal_data['meal_date'] = str(meal_date)

        return serialized_meal_data


class UserFoodHistorySerializer(serializers.ModelSerializer):
    meal = MealDateSerializer(many=True, read_only=True)

    class Meta:
        model = UserFoodHistory
        fields = ('id', 'meal')


class UserSerializer(serializers.ModelSerializer):
    food_history = UserFoodHistorySerializer()

    class Meta:
        model = AppUser
        fields = ('id', 'username', 'email', 'food_history')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_food_history = UserFoodHistory.objects.create()
        user = AppUser.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'], food_history=user_food_history)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
