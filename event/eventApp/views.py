from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RSVP, Event
from .serializers import EventSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import status
# Create your views here.

class EventAPIView(APIView):
    permission_classes = [IsAuthenticated,IsAuthenticatedOrReadOnly]

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
    
class RSVPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = Event.objects.get(pk=event_id)

        if request.user == event.organizer:
            return Response({'detail': 'Organizers cannot RSVP to their own events.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user_event, created = RSVP.objects.get_or_create(user = request.user,event= event)
        if not created:
            return Response({'detail':'You have already RSVP\'d for this event'},status=status.HTTP_400_BAD_REQUEST)
        
        # Check the RSVP status sent in the request data
        rsvp_status = request.data.get('rsvp_status', 'Going')

        if rsvp_status not in ['Going','Not Going','Maybe']:
            return Response({'detail':'Invalid RSVP status.'},status=status.HTTP_400_BAD_REQUEST)
        
        user_event.rsvp_status = rsvp_status
        user_event.save()

        return Response({'detail':f'You have succesfully RSVP\'d as {rsvp_status} for this event'},status=status.HTTP_200_OK)
    
    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'details':'Eent not found'},status=status.HTTP_404_NOT_FOUND)
        rsvps = RSVP.objects.filter(event = event)
        rsvp_data = []

        for rsvp in rsvps:
            user_data = {
                'user_id' : rsvp.user.id,
                'user_username' : rsvp.user.username,
                'rsp_status' : rsvp.rsvp_status
            }
            rsvp_data.append(user_data)

        event_data = {
            'event_id' : event.id,
            'event_name' : event.name,
            'event_description' : event.description,
            'event_date' : event.date,
            'event_time' : event.time,
            'event_location' : event.location,
            'event_category' : event.category,
            'event_oraganizer' : event.organizer.username,
            'rsvps' : rsvp_data
        }

        return Response(event_data, status=status.HTTP_200_OK)