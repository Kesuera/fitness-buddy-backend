from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Workout
from .serializers import WorkoutSerializer


def save_data(serializer, user, success_status):
   if serializer.validated_data['trainer_id'] != user:
      return Response(status=status.HTTP_400_BAD_REQUEST)
   else:
      serializer.save()
      return Response(serializer.data, status=success_status)

@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def create_workout(request):
   user =  request.user
   if user.type != 'trainer':
      return Response(status=status.HTTP_403_FORBIDDEN)

   workout = Workout(trainer_id=user)
   serializer = WorkoutSerializer(workout, data=request.data)

   if serializer.is_valid():
      return save_data(serializer, user, status.HTTP_201_CREATED)
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
      return save_data(serializer, user, status.HTTP_200_OK)
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

   serializer = WorkoutSerializer(workout)
   return Response(serializer.data)

@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def get_workouts(request, user_id):
   return Response('Hello World')
