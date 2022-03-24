from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Workout
from .serializers import WorkoutSerializer


@api_view(['POST', ])
def create_workout(request):
   return Response('Hello World')

@api_view(['PUT', ])
def update_workout(request, workout_id):
   try:
      workout = Workout.objects.get(id=workout_id)
   except Workout.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   serializer = WorkoutSerializer(workout)
   if serializer.is_valid():
      serializer.save()
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
def delete_workout(request, workout_id):
   try:
      workout = Workout.objects.get(id=workout_id)
   except Workout.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   operation = workout.delete()
   if operation:
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', ])
def get_workout_info(request, workout_id):
   try:
      workout = Workout.objects.get(id=workout_id)
   except Workout.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   serializer = WorkoutSerializer(workout)
   return Response(serializer.data)

@api_view(['GET', ])
def get_workouts(request, user_id):
   return Response('Hello World')
