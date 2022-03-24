from django.urls import path
from .views import *


urlpatterns = [
   path('event/create', create_event),
   path('event/update/<int:event_id>/', update_event),
   path('event/delete/<int:event_id>/', delete_event),
   path('event/<int:event_id>/', get_event_info),
   path('event/user/<int:user_id>/', get_events),
]