from django.db import models
from api.user.models import User


class Workout(models.Model):
   class Meta:
      db_table = 'workouts'

   class Type(models.TextChoices):
      full_body = 'full_body',
      lower_body = 'lower_body',
      upper_body = 'upper_body',
      condition = 'condition'

   trainer_id = models.ForeignKey(User, on_delete=models.CASCADE)
   type = models.CharField(max_length=10, choices=Type.choices) 
   name = models.CharField(max_length=100)
   exercises = models.CharField(max_length=100)
   duration = models.IntegerField()
   description = models.CharField(max_length=500)
