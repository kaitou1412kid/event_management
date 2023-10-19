from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import RSVP, Event , Feedback, EventContent
from .serializers import EventSerializer , FeedbackSerializer, EventcontentSerializer
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
    

class FeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'detail':'Event not found.'},status=status.HTTP_404_NOT_FOUND)
        
        feedback = Feedback.objects.filter(event = event)
        serializer = FeedbackSerializer(feedback, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'detail':'Event not found.'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = FeedbackSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, event= event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'detail':'Event not found'},status=status.HTTP_404_NOT_FOUND)
        
        if request.user == event.organizer:

            rsvps = RSVP.objects.filter(event = event)
            rsvp_data = []

            for rsvp in rsvps:
                if rsvp.rsvp_status == 'Going':
                    user_data = {
                    'user_id' : rsvp.user.id,
                    'user_username' : rsvp.user.username,
                    'rsp_status' : rsvp.rsvp_status
                    }
                    rsvp_data.append(user_data)

            attendance = {
                'event_name' : event.name,
                'attendance' : len(rsvp_data),
                'guests' : rsvp_data
            }
            return Response(attendance, status=status.HTTP_200_OK)
        return Response({'details':'You are not the organizer'},status=status.HTTP_400_BAD_REQUEST)
    
class CategoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        category = request.GET.get('category','Ramailo Category')
        event = Event.objects.filter(category = category)
        serializer =  EventSerializer(event, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EventContentView(APIView):
    permission_classes = [IsAuthenticated, IsAuthenticatedOrReadOnly]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'detail':'Event not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == event.organizer:
            serializer = EventcontentSerializer(data = request.data)
            if serializer.is_valid():
                serializer.save(event=event)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'You are not the organizer'},status=status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({'detail':'Event not found'},status=status.HTTP_404_NOT_FOUND)
        
        event_contents = EventContent.objects.filter(event = event)
        content_data = []

        for event_content in event_contents:
            event_data = {
                'image' : event_content.image.url,
                'description' : event_content.description,
                'schedule' : {
                    'start_time' : event_content.start_time,
                    'end_time' : event_content.end_time
                }    
            }
            content_data.append(event_data)

        eventData = {
            'event_name' : event.name,
            'event_description' : event.description,
            'event_date' : event.date,
            'event_time' : event.time,
            'event_content' : content_data
        }
        return Response(eventData, status=status.HTTP_200_OK)
    
    def put(self, request, event_id, content_id):
        try:
            event = Event.objects.get(pk= event_id)
        except Event.DoesNotExist:
            return Response({'detail':'Event not found'},status=status.HTTP_404_NOT_FOUND)
        
        if request.user == event.organizer:
            event_content = EventContent.objects.get(pk=content_id)
            serializer = EventcontentSerializer(event_content,data = request.data, partial=True)
            if serializer.is_valid():
                serializer.save(event=event)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'You are not the organizer'},status=status.HTTP_401_UNAUTHORIZED)
    
    def delete(self, request, event_id,content_id):
        try:
            event = Event.objects.get(pk= event_id)
        except Event.DoesNotExist:
            return Response({'detail':'Event not found'},status=status.HTTP_404_NOT_FOUND)
        if request.user == event.organizer:
            event_content = EventContent.objects.get(pk=content_id)
            event_content.delete()
            return Response({'detail':'Content deleted.'},status=status.HTTP_200_OK)
        return Response({'detail':'You are not the organizer'},status=status.HTTP_401_UNAUTHORIZED)

        

