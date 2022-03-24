from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(models.Model):
   class Meta:
      db_table = 'users'

   class Type(models.TextChoices):
      client = 'client',
      trainer = 'trainer'

   type = models.CharField(max_length=7, choices=Type.choices) 
   username = models.CharField(max_length=100, unique=True)
   full_name = models.CharField(max_length=100)
   email = models.EmailField(unique=True)
   phone_number = PhoneNumberField(unique=True)
   password = models.CharField(max_length=256)
   description = models.CharField(max_length=500, null=True)

class FavouriteTrainer(models.Model):
   class Meta:
      db_table = 'favourite_trainers'

   client_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_id')
   trainer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer_id')