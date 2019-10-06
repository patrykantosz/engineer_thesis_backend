from django.contrib import admin
from .models import AppUser, UserFoodHistory, Meal, FoodDetails


class FoodDetailsInline(admin.TabularInline):
    model = FoodDetails
    extra = 1


class MealAdmin(admin.ModelAdmin):
    inlines = (FoodDetailsInline,)


# Register your models here.
admin.site.register(AppUser)
admin.site.register(UserFoodHistory)
admin.site.register(Meal, MealAdmin)
