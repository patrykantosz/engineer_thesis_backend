from django.urls import path, include
from .api import RegisterAPI, LoginAPI, UserAPI, AddMealAPI, MealListAPI, UserFoodHistoryObjectAPI, MealRetrieveAPI, DeleteFoodProductFromMealAPI
from knox import views as knox_views

urlpatterns = [
    path('api/auth', include('knox.urls')),
    path('api/auth/register', RegisterAPI.as_view(), name="register-endpoint"),
    path('api/auth/login', LoginAPI.as_view(), name="login-endpoint"),
    path('api/auth/user', UserAPI.as_view(), name="get-user-endpoint"),
    path('api/auth/logout', knox_views.LogoutView.as_view(), name="logout-endpoint"),
    path('api/auth/meal', AddMealAPI.as_view(), name="add-new-meal-endpoint"),
    path('api/auth/meal/list', MealListAPI.as_view(), name="list-meals-endpoint"),
    path('api/auth/meal/meal_by_id',
         MealRetrieveAPI.as_view(), name="meal-by-id-endpoint"),
    path('api/auth/food_history/list', UserFoodHistoryObjectAPI.as_view(),
         name="list-food-history-endpoint"),
    path('api/auth/meal/delete', DeleteFoodProductFromMealAPI.as_view(),
         name="meal-delete-food")
]
