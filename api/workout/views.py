from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from .models import Workout
from api.user.models import User
from .serializers import *


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def create_workout(request):
   user =  request.user
   if user.type != 'trainer':
      return Response(status=status.HTTP_403_FORBIDDEN)

   workout = Workout(trainer_id=user)
   serializer = WorkoutSerializer(workout, data=request.data)
   if serializer.is_valid():
<<<<<<< HEAD
      workout = serializer.save()
      data = {
         'id': workout.id,
      }
      return Response(data=data, status=status.HTTP_201_CREATED)
=======
         workout = serializer.save()
         data = {
            'id': workout.id,
         }
         return Response(data=data, status=status.HTTP_201_CREATED)
>>>>>>> 52cf2c4146bd2531ef855c32d417f15ae800c11e
   else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated, ))
def update_workout(request, workout_id):
   user = request.user
   if user.type != 'trainer':
      return Response(status=status.HTTP_403_FORBIDDEN)

   try:
      workout = Workout.objects.get(id=workout_id)
   except Workout.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if workout.trainer_id != user:
      return Response(status=status.HTTP_403_FORBIDDEN)

   serializer = WorkoutSerializer(workout, data=request.data)
   if serializer.is_valid():
<<<<<<< HEAD
      serializer.save()
      return Response(status=status.HTTP_200_OK)
=======
         serializer.save()
         return Response(status=status.HTTP_200_OK)
>>>>>>> 52cf2c4146bd2531ef855c32d417f15ae800c11e
   else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, ))
def delete_workout(request, workout_id):
   user = request.user
   if user.type != 'trainer':
      return Response(status=status.HTTP_403_FORBIDDEN)

   try:
      workout = Workout.objects.get(id=workout_id)
   except Workout.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if workout.trainer_id != user:
      return Response(status=status.HTTP_403_FORBIDDEN)

   operation = workout.delete()
   if operation:
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def get_workout_info(request, workout_id):
   try:
      workout = Workout.objects.get(id=workout_id)
   except Workout.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if request.user.type == 'trainer' and workout.trainer_id != request.user:
      return Response(status=status.HTTP_403_FORBIDDEN)

   serializer = WorkoutSerializer(workout)
   return Response(serializer.data, status=status.HTTP_200_OK)


class WorkoutList(ListAPIView):
   authentication_classes = (TokenAuthentication, )
   permission_classes = (IsAuthenticated, )
   # search_fields = ['type','name']

<<<<<<< HEAD
   def get(self, request, user_id):
      try:
         user = User.objects.get(id=user_id)
      except User.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)

      if (user == request.user):
         pass
      elif (request.user.type == 'trainer' and user.type == 'trainer') or user.type == 'client':
         return Response(status=status.HTTP_403_FORBIDDEN)
=======
   def get(self, request):
      user = request.user
>>>>>>> 52cf2c4146bd2531ef855c32d417f15ae800c11e

      queryset = self.get_queryset(user)
      serializer = WorkoutSimpleSerializer(queryset, many=True)
      return Response(serializer.data, status=status.HTTP_200_OK)

   def get_queryset(self, user):
      if user.type == 'trainer':
         return Workout.objects.filter(trainer_id=user).order_by('name')
      # TODO list workoutov klienta vsetkych jeho favourite trainers
