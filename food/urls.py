from django.urls import path
from .api import AddFoodAPI, ListFoodAPI

urlpatterns = [
    path('api/food/add', AddFoodAPI.as_view(), name="add-food"),
    path('api/food', ListFoodAPI.as_view(), name="foods-all"),
]