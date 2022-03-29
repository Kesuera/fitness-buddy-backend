from rest_framework import serializers
from .models import Meal

class MealSerializer(serializers.ModelSerializer):

   trainer_username = serializers.SerializerMethodField('get_username')
   trainer_full_name = serializers.SerializerMethodField('get_full_name')

   class Meta:
      model = Meal 
      fields = ['id', 'trainer_username','trainer_full_name', 'type', 'name', 'ingredients', 'prep_time', 'description', 'calories', 'photo_path']

   def get_username(self, meal):
      return meal.trainer_id.username

   def get_full_name(self, meal):
      return meal.trainer_id.full_name

class MealSimpleSerializer(serializers.ModelSerializer):
   class Meta:
      model = Meal
      fields = ['id','trainer_id','type','name']