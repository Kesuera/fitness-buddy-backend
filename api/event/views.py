from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Event
from .serializers import EventSerializer


@api_view(['POST', ])
def create_event(request):
   return Response('Hello World')

@api_view(['PUT', ])
def update_event(request, event_id):
   try:
      event = Event.objects.get(id=event_id)
   except Event.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   serializer = EventSerializer(event)
   if serializer.is_valid():
      serializer.save()
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
def delete_event(request, event_id):
   try:
      event = Event.objects.get(id=event_id)
   except Event.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   operation = event.delete()
   if operation:
      return Response(status=status.HTTP_200_OK)
   else:
      return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', ])
def get_event_info(request, event_id):
   try:
      event = Event.objects.get(id=event_id)
   except Event.DoesNotExist:
      return Response(status=status.HTTP_404_NOT_FOUND)

   serializer = EventSerializer(event)
   return Response(serializer.data)

@api_view(['GET', ])
def get_events(request, user_id):
   return Response('Hello World')