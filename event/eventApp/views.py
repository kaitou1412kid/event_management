from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Event
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Create your views here.

class EventAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = EventSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(organizer = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request,):
        event = Event.objects.all()
        serializer = EventSerializer(event, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_event(self, event_id):
        try:
            return Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return None

    def put(self, request, event_id):
        event = self.get_event(event_id)
        if event is not None:
            if request.user == event.organizer:
                serializer = EventSerializer(event, data = request.data)
                if serializer.is_valid():
                    serializer.save(organizer = request.user)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'You do not have permission to edit this eevnt'}, status=status.HTTP_403_FORBIDDEN)
        return Response({'detail' : 'Event not found'}, status=status.HTTP_404_NOT_FOUND)
    
