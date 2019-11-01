from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, MealSerializer, UserFoodHistorySerializer
from .models import AppUser, MealType, FoodDetails, Meal, MealDate
from food.models import Food
from food.serializer import FoodSerializer
from datetime import datetime


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class MealListAPI(generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = MealSerializer

    def get_queryset(self):
        queryset = self.request.user.food_history.meal.all()
        return queryset


class MealRetrieveAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = MealSerializer

    def get_object(self):
        queryset = self.request.user.food_history.meal.all()
        if(self.request.query_params):
            meal_id = self.request.query_params.get('meal_id', '')
            return queryset.get(pk=meal_id)


class UserFoodHistoryObjectAPI(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserFoodHistorySerializer

    def get_object(self):
        return self.request.user.food_history


class AddMealAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def post(self, request, *args, **kwargs):
        food_id = request.data.get('food_id', False)
        food_weight = request.data.get('food_weight', False)
        meal_type = request.data.get('meal_type', False)
        meal_date = datetime.strptime(request.data.get(
            'meal_date', False), "%Y-%m-%d").date()

        meal_type_enum = MealType.get(meal_type)

        food = Food.objects.get(id=food_id)
        user = self.request.user
        user_history = user.food_history

        food_final = None
        meal = None
        meal_final = None

        meals_by_meal_type = self.request.user.food_history.meal.filter(
            meal_type=meal_type_enum)
        if(len(meals_by_meal_type) != 0):
            for meal_by_type in meals_by_meal_type:
                meal_to_get_date = self.request.user.food_history.mealdate_set.get(
                    meal=meal_by_type)
                if(meal_to_get_date.meal_date == meal_date):
                    food_final = FoodDetails(
                        meal=meal_by_type, food=food, food_weight=food_weight)
                else:
                    meal = Meal.objects.create(meal_type=meal_type_enum)
                    food_final = FoodDetails(
                        meal=meal, food=food, food_weight=food_weight)
                    meal_final = MealDate(
                        user_food_history=user_history, meal=meal, meal_date=meal_date)
                    meal_final.save()
        else:
            meal = Meal.objects.create(meal_type=meal_type_enum)
            food_final = FoodDetails(
                meal=meal, food=food, food_weight=food_weight)
            meal_final = MealDate(
                user_food_history=user_history, meal=meal, meal_date=meal_date)
            meal_final.save()

        food_final.save()

        serializer = UserFoodHistorySerializer(user_history)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeleteFoodProductFromMeal(generics.DestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def delete(self, request, *args, **kwargs):
        food_details_id = request.data.get('food_details_id', False)
        meal_id = request.data.get('meal_id', False)
        user = self.request.user
        user_history = user.food_history
