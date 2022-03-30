from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
   path('meal/create', create_meal),
   path('meal/update/<int:meal_id>', update_meal),
   path('meal/delete/<int:meal_id>', delete_meal),
   path('meal/<int:meal_id>', get_meal_info),
   path('meal/user/<int:user_id>', MealList.as_view()),
   path('meal/image/meal_photos/<str:photo_name>', get_image)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)