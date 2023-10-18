from celery import shared_task
from django.core.mail import send_mail
from .models import Event, RSVP
from django.utils import timezone
from django.conf import settings
#sending mail as reminders

@shared_task
def send_event_reminders():
    tommorow = timezone.now() + timezone.timedelta(days=1)
    print("tomorrow",tommorow)
    events_to_remind = Event.objects.filter(date=tommorow)

    for event in events_to_remind:
        participants = RSVP.objects.filter(event = event)

        for participant in participants:
            send_mail(
                f'Reminder: {event.name}',
                f"Don't forget , your event {event.name} is happening tomorrow at {event.time}!",
                settings.EMAIL_HOST_USER,
                [participant.user.email],
                fail_silently=False
            )

    return "Done"
