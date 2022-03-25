from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *


urlpatterns = [
   path('user/register', register_user),
   path('user/login', obtain_auth_token),
   path('user/update/<int:user_id>', update_user),
   path('user/<int:user_id>', get_user_info),
   path('user/trainer', TrainerList.as_view()),
   path('user/trainer/<str:trainer_name>', TrainerList.as_view()),
   path('user/fav_trainer/follow', follow_trainer),
   path('user/fav_trainer/unfollow/<int:record_id>', unfollow_trainer),
   path('user/fav_trainer/<int:user_id>', FavouriteTrainerList.as_view()),
]