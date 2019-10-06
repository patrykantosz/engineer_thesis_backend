from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AppUser, UserFoodHistory, Meal, FoodDetails
from food.serializer import FoodSerializer
from django.core import serializers as coreserializers
from food.models import Food


class FoodDetailsSerializer(serializers.ModelSerializer):
    food = serializers.ReadOnlyField(source='food.id')

    class Meta:
        model = FoodDetails
        fields = ('id', 'food', 'food_weight')


class MealSerializer(serializers.ModelSerializer):
    food = FoodDetailsSerializer(source='fooddetails_set', many=True)

    class Meta:
        model = Meal
        fields = ('id', 'meal_type', 'food')


class UserFoodHistorySerializer(serializers.ModelSerializer):
    meal = MealSerializer(many=True)

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
