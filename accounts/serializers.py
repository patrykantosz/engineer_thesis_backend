from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import AppUser, UserFoodHistory, Meal, FoodDetails, MealDate, UserBodyParameters, UserNutritionsTarget
from food.serializer import FoodSerializer
from django.core import serializers as coreserializers
from food.models import Food
from django.db.models.query import QuerySet


class FoodDetailsSerializer(serializers.RelatedField):

    previous = []
    index = 0

    def to_representation(self, value):
        self.index += 1
        if type(self.root.instance) == QuerySet:
            self.root.instance = self.root.instance[0]
        food_details_object = FoodDetails.objects.all()
        food_details = FoodDetails.objects.filter(
            food=value, meal=self.root.instance).first()
        if food_details in self.previous:
            for food_detail in self.previous:
                food_details_object = food_details_object.exclude(
                    pk=food_detail.id)
            food_details = food_details_object.filter(
                food=value, meal=self.root.instance).first()
            self.previous.append(food_details)
        else:
            self.previous.append(food_details)
        food_weight = food_details.food_weight
        value = FoodSerializer(value)
        serialized_food_data = value.data
        serialized_food_data['food_details_id'] = str(food_details.id)
        serialized_food_data['food_weight'] = str(food_weight)
        if(self.index == len(FoodDetails.objects.filter(meal=self.root.instance))):
            self.previous.clear()
            self.index = 0

        return serialized_food_data


class MealSerializer(serializers.ModelSerializer):
    food = FoodDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = ('id', 'meal_type', 'food')


class MealDateSerializer(serializers.RelatedField):
    def to_representation(self, value):
        if type(self.root.instance) is AppUser:
            self.root.instance = self.root.instance.food_history
        if type(self.root.instance) == QuerySet:
            self.root.instance = self.root.instance[0]
        meal_date_object = MealDate.objects.filter(
            meal=value, user_food_history=self.root.instance).first()
        meal_date = meal_date_object.meal_date
        value = MealSerializer(value)
        serialized_meal_data = value.data
        serialized_meal_data['meal_date_id'] = str(meal_date_object.id)
        serialized_meal_data['meal_date'] = str(meal_date)
        serialized_meal_data.move_to_end('meal_date_id', last=False)
        serialized_meal_data.move_to_end('meal_date', last=False)

        return serialized_meal_data


class UserFoodHistorySerializer(serializers.ModelSerializer):
    meal = MealDateSerializer(many=True, read_only=True)

    class Meta:
        model = UserFoodHistory
        fields = ('id', 'meal')


class UserBodyParametersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBodyParameters
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.user_weight = validated_data.get(
            'user_weight', instance.user_weight)
        instance.user_height = validated_data.get(
            'user_height', instance.user_height)
        instance.user_bmi = validated_data.get('user_bmi', instance.user_bmi)
        instance.save()
        return instance


class UserNutritionsTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNutritionsTarget
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.target_calories = validated_data.get(
            'target_calories', instance.target_calories)
        instance.target_carbohydrates = validated_data.get(
            'target_carbohydrates', instance.target_carbohydrates)
        instance.target_proteins = validated_data.get(
            'target_proteins', instance.target_proteins)
        instance.target_fats = validated_data.get(
            'target_fats', instance.target_fats)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    food_history = UserFoodHistorySerializer()
    body_parameters = UserBodyParametersSerializer()
    nutritions_target = UserNutritionsTargetSerializer()

    class Meta:
        model = AppUser
        fields = ('id', 'username', 'email', 'body_parameters',
                  'nutritions_target', 'food_history')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_food_history = UserFoodHistory.objects.create()
        user_body_parameters = UserBodyParameters.objects.create()
        user_nutritions_target = UserNutritionsTarget.objects.create()
        user = AppUser.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'], food_history=user_food_history, body_parameters=user_body_parameters, nutritions_target=user_nutritions_target)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")
