from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserManager(BaseUserManager):
   def create_user(self, type, username, full_name, email, phone_number, password):
      if not type:
         raise ValueError("User must have a type.")
      if not username:
         raise ValueError("User must have a username.")
      if not full_name:
         raise ValueError("User must have a full name.")
      if not email:
         raise ValueError("User must have an email address.")
      if not phone_number:
         raise ValueError("User must have a phone number.")
      if not password:
         raise ValueError("User must have a password.")

      user = self.model(
         type=type, 
         username=username, 
         full_name=full_name,
         email=self.normalize_email(email),
         phone_number=phone_number
      )
      
      user.set_password(password)
      user.save(using=self._db)
      return user

   def create_superuser(self, type, username, full_name, email, phone_number, password):
      user = self.create_user(
         type=type,
         username=username,
         full_name=full_name,
         email=email,
         phone_number=phone_number,
         password=password
      )

      user.is_admin = True
      user.is_staff = True
      user.is_superuser = True
      user.save(using=self.db)
      return user


class User(AbstractBaseUser):
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

   # required AbstractBaseUser fields
   date_joined = models.DateTimeField(auto_now_add=True)
   last_login = models.DateTimeField(auto_now=True)
   is_admin = models.BooleanField(default=False)
   is_active = models.BooleanField(default=True)
   is_staff = models.BooleanField(default=False)
   is_superuser = models.BooleanField(default=False)

   USERNAME_FIELD = 'username'
   REQUIRED_FIELDS = ['type', 'full_name', 'email', 'phone_number', 'password']

   objects = UserManager()

   def __str__(self):
      return self.username

   def get_type(self):
      return self.type

   def has_perm(self, perm, obj=None):
      return self.is_admin
   
   def has_module_perms(self, app_label):
      return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
   if created:
      Token.objects.create(user=instance)


class FavouriteTrainer(models.Model):
   class Meta:
      db_table = 'favourite_trainers'

   client_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='client_id')
   trainer_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer_id')
