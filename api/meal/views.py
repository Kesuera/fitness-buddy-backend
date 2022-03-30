from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from .models import Meal
from api.user.models import User
from .serializers import MealSerializer, MealSimpleSerializer
from api.user.models import FavouriteTrainer
from django.http import FileResponse


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def create_meal(request):

    user = request.user
    if user.type != 'trainer':
        return Response(status =status.HTTP_403_FORBIDDEN)

    meal = Meal(trainer_id=user)
    serializer = MealSerializer(meal, data=request.data)
    if serializer.is_valid():
        meal = serializer.save()
        data = {
            'id': meal.id
        }
        return Response(data =data, status =status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated, ))
def update_meal(request, meal_id):
    user = request.user
    if user.type != 'trainer':
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        meal = Meal.objects.get(id=meal_id)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if meal.trainer_id != user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = MealSerializer(meal, data =request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, ))
def delete_meal(request, meal_id):
    user = request.user
    if user.type != 'trainer':
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        meal = Meal.objects.get(id=meal_id)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if meal.trainer_id != user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    operation = meal.delete()
    if operation:
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def get_meal_info(request, meal_id):
    try:
        meal = Meal.objects.get(id=meal_id)
    except Meal.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.user.type == 'trainer' and meal.trainer_id != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    serializer = MealSerializer(meal)
    return Response(serializer.data, status=status.HTTP_200_OK)

#@api_view(['GET', ])
#@permission_classes((IsAuthenticated, ))
#def imageGet(instance, request, name):
#    location = '/meal_photos/{trainer_id}/'+name.format(trainer_id=str(instance.trainer_id),filename=name)
#    print(location)
#    try:
#        img = open(location, 'rb')
#        resp = FileResponse(img)
#        resp.status_code = 200
#        return resp
#    except IOError:
#        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class MealList(ListAPIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if (user == request.user):
            pass
        elif (request.user.type == 'trainer' and user.type == 'trainer') or user.type == 'client':
            return Response(status=status.HTTP_403_FORBIDDEN)

        queryset = self.get_queryset(user)
        serializer = MealSimpleSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self, user):
        if user.type == 'trainer':
            return Meal.objects.filter(trainer_id=user).order_by('name')
        else:
            trainers = FavouriteTrainer.objects.filter(client_id=user).values_list('trainer_id')
            return Meal.objects.filter(trainer_id__in=trainers).order_by('name')
