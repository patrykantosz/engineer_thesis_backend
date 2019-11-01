from django.urls import path
from .api import AddFoodAPI, ListFoodAPI, FoodRetrieveAPI

urlpatterns = [
    path('api/food/add', AddFoodAPI.as_view(), name="add-food"),
    path('api/food/', ListFoodAPI.as_view(), name="foods-all"),
    path('api/food/food_by_id', FoodRetrieveAPI.as_view(), name="food-by-id"),
]
