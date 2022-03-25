from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer


@api_view(['POST', ])
def register_user(request):
   serializer = RegistrationSerializer(data=request.data)
   if serializer.is_valid():
      user = serializer.save()
      data = {
         'type': user.type,
         'username': user.username,
         'full_name': user.full_name,
         'email': user.email,
         'phone_number': str(user.phone_number),
         'token': Token.objects.get(user=user).key
      }
      return Response(data=data, status=status.HTTP_201_CREATED)
   else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', ])
def login_user(request):
   return Response('Hello World')

@api_view(['PUT', ])
def update_user(request, user_id):
   return Response('Hello World')

@api_view(['GET', ])
def get_user_info(request, user_id):
   return Response('Hello World')

@api_view(['GET', ])
def get_trainers(request, trainer_name):
   return Response('Hello World')

@api_view(['POST', ])
def create_fav_trainer(request):
   return Response('Hello World')

@api_view(['DELETE', ])
def delete_fav_trainer(request, trainer_id):
   return Response('Hello World')

@api_view(['GET', ])
def get_fav_trainers(request, client_id):
   return Response('Hello World')