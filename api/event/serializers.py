from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
   class Meta:
      model = Event
      fields = ['id', 'trainer_id', 'name', 'place', 'date', 'duration', 'price', 'description']