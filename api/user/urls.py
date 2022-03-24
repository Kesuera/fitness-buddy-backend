from django.urls import path
from .views import *


urlpatterns = [
   path('user/register', register_user),
   path('user/login/', login_user),
   path('user/update/<int:user_id>/', update_user),
   path('user/<int:user_id>/', get_user_info),
   path('user/trainer/<str:trainer_name>/', get_trainers),
   path('user/fav_trainer/create', create_fav_trainer),
   path('user/fav_trainer/delete/<int:trainer_id>/', delete_fav_trainer),
   path('user/fav_trainer/<int:client_id>/', get_fav_trainers),
]