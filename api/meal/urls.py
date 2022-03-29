from django.urls import path
from .views import *


urlpatterns = [
   path('meal/create', create_meal),
   path('meal/update/<int:meal_id>', update_meal),
   path('meal/delete/<int:meal_id>', delete_meal),
   path('meal/<int:meal_id>', get_meal_info),

   path('meal/user', MealList.as_view()),
]