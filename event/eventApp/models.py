from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    category = models.CharField(max_length=50)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name