from rest_framework import serializers
from django.contrib.auth.models import BaseUserManager
from .models import User, FavouriteTrainer
import re

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

      if not user.username.isalnum():
         raise serializers.ValidationError({'username': 'Username can only contains letters and numbers without white spaces.'})

      if len(user.username) < 4:
         raise serializers.ValidationError({'username': 'Username must be atleast 4 characters long.'})

      if not all(x.isalpha() or x.isspace() for x in user.full_name):
         raise serializers.ValidationError({'full_name': 'Full name can only contain letters.'})

      if len(user.full_name) < 4:
         raise serializers.ValidationError({'full_name': 'Full name must be atleast 4 characters long.'})

      if len(password) < 6:
         raise serializers.ValidationError({'password': 'Password must be atleast 6 characters long.'})

      if password != password_again:
         raise serializers.ValidationError({'password': 'Passwords must match.'})

      user.set_password(password)
      user.save()
      return user


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id', 'type', 'username', 'full_name', 'email', 'phone_number', 'description']


class UserSimpleSerializer(serializers.ModelSerializer):
   is_fav = serializers.SerializerMethodField('get_is_fav')
   
   class Meta:
      model = User
      fields = ['id', 'username', 'full_name', 'is_fav']

   def get_is_fav(self, trainer):
      client_id = self.context.get('client_id')
      try:
         FavouriteTrainer.objects.get(client_id=client_id, trainer_id=trainer.id)
         return True
      except FavouriteTrainer.DoesNotExist:
         return False

class UserUpdateSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['email', 'phone_number', 'description']

   def save(self, user):
      user.email = BaseUserManager.normalize_email(self.validated_data['email'])
      user.phone_number = self.validated_data['phone_number']
      description =  re.sub(' +', ' ', self.validated_data['description']).strip()
      if (len(description) < 10 or len(description) > 500):
         raise serializers.ValidationError({'description': 'Description must be 10-500 characters long.'})
      user.description = description
      user.save()
      return user


class FavouriteTrainerSerializer(serializers.ModelSerializer):
   class Meta:
      model = FavouriteTrainer 
      fields = ['id', 'client_id', 'trainer_id']
      

class FavouriteTrainerInfoSerializer(serializers.ModelSerializer):
   trainer_username = serializers.SerializerMethodField('get_trainer_username')
   trainer_full_name = serializers.SerializerMethodField('get_trainer_full_name')

   class Meta:
      model = FavouriteTrainer 
      fields = ['trainer_id', 'trainer_username', 'trainer_full_name']

   def get_trainer_username(self, fav_trainer):
      return fav_trainer.trainer_id.username

   def get_trainer_full_name(self, fav_trainer):
      return fav_trainer.trainer_id.full_name


class FollowerInfoSerializer(serializers.ModelSerializer):
   client_username = serializers.SerializerMethodField('get_client_username')
   client_full_name = serializers.SerializerMethodField('get_client_full_name')

   class Meta:
      model = FavouriteTrainer 
      fields = ['client_id', 'client_username', 'client_full_name']

   def get_client_username(self, fav_trainer):
      return fav_trainer.client_id.username

   def get_client_full_name(self, fav_trainer):
      return fav_trainer.client_id.full_name