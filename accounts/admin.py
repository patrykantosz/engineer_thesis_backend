from django.contrib import admin
from .models import AppUser, UserFoodHistory, Meal, FoodDetails, MealDate, UserNutritionsTarget, UserBodyParameters, MealDate, FoodDetails


class FoodDetailsInline(admin.TabularInline):
    model = FoodDetails
    extra = 1


class MealAdmin(admin.ModelAdmin):
    inlines = (FoodDetailsInline,)


class MealDateInline(admin.TabularInline):
    model = MealDate
    extra = 1


class UserFoodHistoryAdmin(admin.ModelAdmin):
    inlines = (MealDateInline,)


# Register your models here.
admin.site.register(AppUser)
admin.site.register(UserBodyParameters)
admin.site.register(UserNutritionsTarget)
admin.site.register(MealDate)
admin.site.register(FoodDetails)
admin.site.register(UserFoodHistory, UserFoodHistoryAdmin)
admin.site.register(Meal, MealAdmin)
