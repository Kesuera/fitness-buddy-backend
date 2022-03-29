from django.urls import path
from .views import *


urlpatterns = [
   path('user/register', register_user),
   path('user/login', LoginAuthToken.as_view()),
   path('user/logout', logout_user),
   path('user/update', update_user),
   path('user/<int:user_id>', get_user_info),
   path('user/trainer', TrainerList.as_view()),
   path('user/trainer/<str:trainer_name>', TrainerList.as_view()),
   path('user/favourites/follow/<int:trainer_id>', follow_trainer),
   path('user/favourites/unfollow/<int:trainer_id>', unfollow_trainer),
   path('user/favourites', FavouriteTrainerList.as_view()),
]