from rest_framework import serializers
from .models import Event,RSVP, Feedback, EventContent

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = ['rsvp_status']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['rating','comment']

class EventcontentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventContent
        fields = ['description','image','start_time', 'end_time']