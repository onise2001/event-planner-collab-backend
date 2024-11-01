from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Notification, RSVP, Event



@shared_task
def send_event_notifications():
    current_time = timezone.now()
    one_hour_from_now = current_time + timedelta(hours=1)
    upcoming_events = Event.objects.filter(startDate__gte=current_time, startDate__lte=one_hour_from_now)

    for event in upcoming_events:
        rsvps = RSVP.objects.filter(event=event)

        for rsvp in rsvps:
            Notification.objects.create(
                sender=event.organizer,
                receiver=rsvp.user,
                message=f"Reminder: '{event.title}' is starting in one hour at {event.startDate.strftime('%I:%M %p')}!"
            ).save()