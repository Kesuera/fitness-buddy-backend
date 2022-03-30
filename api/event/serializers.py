from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):

   trainer_username = serializers.SerializerMethodField('get_username')
   trainer_full_name = serializers.SerializerMethodField('get_full_name')

   class Meta:
      model = Event
      fields = ['id','trainer_full_name','trainer_username', 'name', 'place', 'date', 'duration', 'price', 'description']

   def get_username(self, workout):
      return workout.trainer_id.username

   def get_full_name(self, workout):
      return workout.trainer_id.full_name

class EventSimpleSerializer(serializers.ModelSerializer):
   class Meta:
      model = Event
      fields = ['id', 'name']