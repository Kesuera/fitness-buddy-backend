from django.urls import path
from .views import *


urlpatterns = [
   path('workout/create', create_workout),
   path('workout/update/<int:workout_id>', update_workout),
   path('workout/delete/<int:workout_id>', delete_workout),
   path('workout/<int:workout_id>', get_workout_info),
   path('workout/user/<int:user_id>/', get_workouts),
]