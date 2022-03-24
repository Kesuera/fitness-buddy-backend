from rest_framework import serializers
from .models import Workout

class WorkoutSerializer(serializers.ModelSerializer):
   class Meta:
      model = Workout 
      fields = ['id', 'trainer_id', 'type', 'name', 'exercises', 'duration']