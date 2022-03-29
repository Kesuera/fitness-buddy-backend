from django.db import models
from api.user.models import User

def upload_location(instance, filename, **kwargs):
   file_path = 'meal/{trainer_id}/{filename}'.format(
      trainer_id=str(instance.trainer_id), filename=filename
   )
   return file_path

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
   description = models.CharField(max_length=500)
   photo_path = models.ImageField(upload_to=upload_location, null=True, blank=False)

   def __str__(self):
      return self.name
