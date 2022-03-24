from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, FavouriteTrainer


class RegistrationSerializer(serializers.ModelSerializer):
   password_again = serializers.CharField(style={'input_type': 'password'}, max_length=200, write_only=True)

   class Meta:
      model = User
      fields = ['type', 'username', 'full_name', 'email', 'phone_number', 'password', 'password_again']
      extra_kwargs = {
         'password': {'write_only': True},
         'password': {'style': {'input_type': 'password'}}
      }
   
   def save(self):
      user = User(
         type = self.validated_data['type'],
         username = self.validated_data['username'],
         full_name = self.validated_data['full_name'],
         email = self.validated_data['email'],
         phone_number = self.validated_data['phone_number'],
      )
      password = self.validated_data['password']
      password_again = self.validated_data['password_again']

      if password != password_again:
         raise serializers.ValidationError({'password': 'Passwords must match.'})
      user.password = make_password(password)
      user.save()
      return user

class FavouriteTrainerSerializer(serializers.ModelSerializer):
   class Meta:
      model = FavouriteTrainer 
      fields = ['id', 'client_id', 'trainer_id']
