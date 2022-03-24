from rest_framework import serializers
from .models import Meal

class MealSerializer(serializers.ModelSerializer):
   class Meta:
      model = Meal 
      fields = ['id', 'trainer_id', 'type', 'name', 'ingredients', 'prep_time', 'description', 'calories', 'photo_path']