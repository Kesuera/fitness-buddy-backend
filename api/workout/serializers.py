from rest_framework import serializers
from .models import Workout

class WorkoutSerializer(serializers.ModelSerializer):
   trainer_username = serializers.SerializerMethodField('get_username')
   trainer_full_name = serializers.SerializerMethodField('get_full_name')

   class Meta:
      model = Workout 
      fields = ['id', 'trainer_id', 'trainer_username', 'trainer_full_name', 'type', 'name', 'exercises', 'duration', 'description']

   def get_username(self, workout):
      return workout.trainer_id.username

   def get_full_name(self, workout):
      return workout.trainer_id.full_name

class WorkoutSimpleSerializer(serializers.ModelSerializer):
   class Meta:
      model = Workout
      fields = ['trainer_id', 'type', 'name']
