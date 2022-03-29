from rest_framework import serializers
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
      user.set_password(password)
      user.save()
      return user


class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id', 'type', 'username', 'full_name', 'email', 'phone_number']


class UserSimpleSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['id', 'username', 'full_name']


class UserUpdateSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = ['email', 'phone_number', 'description']


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