from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from .models import User, FavouriteTrainer
from .serializers import *


@api_view(['POST', ])
def register_user(request):
   serializer = RegistrationSerializer(data=request.data)
   if serializer.is_valid():
      user = serializer.save()
      data = UserSerializer(user).data
      data ['token'] = Token.objects.get(user=user).key
      return Response(data=data, status=status.HTTP_201_CREATED)
   else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAuthToken(ObtainAuthToken):
   def post(self, request):
      serializer = self.serializer_class(data=request.data, context={'request': request})
      serializer.is_valid(raise_exception=True)
      user = serializer.validated_data['user']
      token, _ = Token.objects.get_or_create(user=user)
      data = UserSerializer(user).data
      data['token'] = token.key
      return Response(data=data, status=status.HTTP_200_OK)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, ))
def logout_user(request):
   operation = request.user.auth_token.delete()
   if operation:
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated, ))
def update_user(request):
   user = request.user
   serializer = UserUpdateSerializer(user, data=request.data)
   if serializer.is_valid():
      serializer.save(user)
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def get_user_info(request, user_id):
   try:
      user = User.objects.get(id=user_id)
   except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if request.user != user:
      if request.user.type == 'trainer':
         try:
            FavouriteTrainer.objects.get(client_id=user_id, trainer_id=request.user)
         except FavouriteTrainer.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)

      if request.user.type == 'client' and user.type == 'client':
         return Response(status=status.HTTP_403_FORBIDDEN)

   serializer = UserSerializer(user)
   return Response(serializer.data, status=status.HTTP_200_OK)


class TrainerList(ListAPIView):
   authentication_classes = (TokenAuthentication, )
   permission_classes = (IsAuthenticated, )

   def get(self, request, trainer_name=None):
      user = request.user
      if user.type != 'client':
         return Response(status=status.HTTP_403_FORBIDDEN)

      queryset = self.get_queryset(trainer_name)
      serializer = UserSimpleSerializer(queryset, many=True, context={'client_id': user.id})
      return Response(serializer.data, status=status.HTTP_200_OK)

   def get_queryset(self, trainer_name):
      if trainer_name:
         return User.objects.filter(Q(type='trainer') & (Q(username__icontains=trainer_name) | Q(full_name__icontains=trainer_name))).order_by('full_name')
      else:
         return User.objects.filter(type='trainer').order_by('full_name')


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def follow_trainer(request, trainer_id):
   user =  request.user
   if user.type != 'client':
      return Response(status=status.HTTP_403_FORBIDDEN)

   try:
      trainer = User.objects.get(id=trainer_id, type='trainer')
   except User.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   data = {
      'client_id': user.id,
      'trainer_id': trainer.id,
   }
   fav_trainer = FavouriteTrainer()
   serializer = FavouriteTrainerSerializer(fav_trainer, data=data)
   if serializer.is_valid():
      fav_trainer = serializer.save()
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, ))
def unfollow_trainer(request, trainer_id):
   user = request.user
   if user.type != 'client':
      return Response(status=status.HTTP_403_FORBIDDEN)

   try:
      fav_trainer = FavouriteTrainer.objects.get(client_id=user.id, trainer_id=trainer_id)
   except FavouriteTrainer.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   operation = fav_trainer.delete()
   if operation:
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FavouriteTrainerList(ListAPIView):
   authentication_classes = (TokenAuthentication, )
   permission_classes = (IsAuthenticated, )

   def get(self, request):
      user = request.user
      queryset = self.get_queryset(user)

      if user.type == 'client':
         serializer = FavouriteTrainerInfoSerializer(queryset, many=True)
         data = sorted(serializer.data, key=lambda k: k['trainer_full_name'])
      else:
         serializer = FollowerInfoSerializer(queryset, many=True)
         data = sorted(serializer.data, key=lambda k: k['client_full_name'])
      
      return Response(data, status=status.HTTP_200_OK)

   def get_queryset(self, user):
      if user.type == 'client':
         return FavouriteTrainer.objects.filter(client_id=user)
      else:
         return FavouriteTrainer.objects.filter(trainer_id=user)