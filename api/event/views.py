from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from .models import Event
from api.user.models import User
from .serializers import EventSerializer, EventSimpleSerializer


@api_view(['POST', ])
@permission_classes((IsAuthenticated, ))
def create_event(request):
   user = request.user
   if user.type != 'trainer':
      return Response(status=status.HTTP_403_FORBIDDEN)

   event = Event(trainer_id=user)
   serializer = EventSerializer(event, data=request.data)
   if serializer.is_valid():
      event = serializer.save()
      data = {
         'id': event.id,
      }
      return Response(data=data, status=status.HTTP_201_CREATED)
   else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT', ])
@permission_classes((IsAuthenticated, ))
def update_event(request, event_id):
   user = request.user
   if user.type != 'trainer':
      return Response(status=status.HTTP_403_FORBIDDEN)
   try:
      event = Event.objects.get(id=event_id)
   except Event.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if event.trainer_id != user:
      return Response(status=status.HTTP_403_FORBIDDEN)

   serializer = EventSerializer(event, data=request.data)
   if serializer.is_valid():
      serializer.save()
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated, ))
def delete_event(request, event_id):
   user = request.user
   if user.type != 'trainer':
      return Response(status=status.HTTP_403_FORBIDDEN)
   try:
      event = Event.objects.get(id=event_id)
   except Event.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if event.trainer_id != user:
      return Response(status=status.HTTP_403_FORBIDDEN)

   operation = event.delete()
   if operation:
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', ])
@permission_classes((IsAuthenticated, ))
def get_event_info(request, event_id):
   try:
      event = Event.objects.get(id=event_id)
   except Event.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   if request.user.type == 'trainer' and event.trainer_id != request.user:
      return Response(status=status.HTTP_403_FORBIDDEN)

   serializer = EventSerializer(event)
   return Response(serializer.data, status=status.HTTP_200_OK)


class EventList(ListAPIView):
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
         serializer = EventSimpleSerializer(queryset, many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)

      def get_queryset(self, user):
         if user.type == 'trainer':
            return Event.objects.filter(trainer_id=user).order_by('date')
         elif user.type == 'client':
            return Event.objects.filter()
