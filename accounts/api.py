from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, FoodDetailsSerializer, MealSerializer, UserFoodHistorySerializer, UserNutritionsTargetSerializer, UserBodyParametersSerializer
from .models import AppUser, MealType, FoodDetails, Meal, MealDate, UserBodyParameters, UserNutritionsTarget
from food.models import Food
from food.serializer import FoodSerializer
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist


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


class FoodDetailsUpdateAPI(generics.UpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    serializer_class = MealSerializer
    queryset = FoodDetails.objects.all()

    def partial_update(self, request, *args, **kwargs):
        food_weight = request.data.get('food_weight', False)
        food_details_id = request.data.get('food_details_id', False)
        try:
            instance = FoodDetails.objects.get(pk=food_details_id)
        except ObjectDoesNotExist:
            error_response = "FoodDetail with id "
            error_response += str(food_details_id)
            error_response += " doesn't exist"
            return Response({
                "message": error_response,
            }, status=status.HTTP_400_BAD_REQUEST)
        instance.food_weight = food_weight
        instance.save()
        if(instance.food_weight == food_weight):
            return Response({
                'message': 'Update done',
            }, status=status.HTTP_200_OK)
        return Response({
            'message': 'Update failed',
        }, status=status.HTTP_404_NOT_FOUND)


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
            object_created = False
            for meal_by_type in meals_by_meal_type:
                meal_to_get_date = self.request.user.food_history.mealdate_set.get(
                    meal=meal_by_type)
                if(meal_to_get_date.meal_date == meal_date):
                    food_final = FoodDetails(
                        meal=meal_by_type, food=food, food_weight=food_weight)
                    object_created = True
            if(not object_created):
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


class DeleteFoodProductFromMealAPI(generics.DestroyAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def delete(self, request, *args, **kwargs):
        if(self.request.query_params):
            food_details_id = self.request.query_params.get(
                'food_details_id', False)
            if(food_details_id):
                try:
                    food_details_object = FoodDetails.objects.get(
                        pk=food_details_id)
                except ObjectDoesNotExist:
                    error_response = "FoodDetail with id "
                    error_response += str(food_details_id)
                    error_response += " doesn't exist"
                    return Response({
                        "message": error_response,
                    }, status=status.HTTP_400_BAD_REQUEST)
                if(food_details_object):
                    meal_parent = food_details_object.meal
                    food_details_object.delete()
                    meal_parent_food_queryset = meal_parent.food.all()
                    if(len(meal_parent_food_queryset) == 0):
                        meal_parent.delete()
                    return Response({
                        "message": "Delete food done",
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        "message": "Delete food failed",
                    }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "message": "No query params or query params are wrong",
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class UserBodyParametersAPI(generics.RetrieveUpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserBodyParametersSerializer

    def get_object(self):
        return self.request.user.body_parameters

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class UserNutritionsTargetAPI(generics.RetrieveUpdateAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    serializer_class = UserNutritionsTargetSerializer

    def get_object(self):
        return self.request.user.nutritions_target

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
