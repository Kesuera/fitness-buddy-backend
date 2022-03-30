from django.db import models
from api.user.models import User


class Event(models.Model):
   class Meta:
      db_table = 'events'

   trainer_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='trainer_id')
   name = models.CharField(max_length=100)
   place = models.CharField(max_length=100)
   date = models.DateTimeField()
   duration = models.IntegerField()
   price = models.IntegerField()
   description = models.CharField(max_length=500)
