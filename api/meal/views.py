from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Meal
from .serializers import MealSerializer


@api_view(['POST', ])
def create_meal(request):
   return Response('Hello World')

@api_view(['PUT', ])
def update_meal(request, meal_id):
   try:
      meal = Meal.objects.get(id=meal_id)
   except Meal.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   serializer = MealSerializer(meal)
   if serializer.is_valid():
      serializer.save()
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
def delete_meal(request, meal_id):
   try:
      meal = Meal.objects.get(id=meal_id)
   except Meal.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   operation = meal.delete()
   if operation:
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', ])
def get_meal_info(request, meal_id):
   try:
      meal = Meal.objects.get(id=meal_id)
   except Meal.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   serializer = MealSerializer(meal)
   return Response(serializer.data)

@api_view(['GET', ])
def get_meals(request, user_id):
   return Response('Hello World')

