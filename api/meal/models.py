from django.db import models
from api.user.models import User

class Meal(models.Model):
   class Meta:
      db_table = 'meals'

   class Type(models.TextChoices):
      breakfast = 'breakfast',
      lunch = 'lunch', 
      dinner = 'dinner',
      desert = 'desert'

   trainer_id = models.ForeignKey(User, on_delete=models.CASCADE)
   type = models.CharField(max_length=10, choices=Type.choices) 
   name = models.CharField(max_length=100)
   ingredients = models.CharField(max_length=100)
   prep_time = models.IntegerField()
   calories = models.IntegerField()
   duration = models.IntegerField()
   description = models.CharField(max_length=500)
   photo_path = models.FilePathField(max_length=100, unique=True)
