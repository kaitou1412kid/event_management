from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    
class RSVP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rsvp_status = models.CharField(
        max_length=10,
        choices=[('Going','Going'), ('Not Going','Not Going'),('Maybe','Maybe')],
        default='Maybe'
    )

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1),MaxValueValidator(5)]
    )
    comment = models.TextField()

class EventContent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/')
    start_time = models.TimeField()
    end_time = models.TimeField()
