from django.urls import path, include
from .views import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
   path('meal/create', create_meal),
   path('meal/update/<int:meal_id>', update_meal),
   path('meal/delete/<int:meal_id>', delete_meal),
   path('meal/<int:meal_id>', get_meal_info),
   path('meal/user/<int:user_id>', MealList.as_view()),
   #url(r'^upload_img', UploadedImageAPIView.as_view())
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)