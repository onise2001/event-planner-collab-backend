from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.TextField()

class Privacy(models.Model):
    name = models.TextField()

class Medium(models.Model):
    name = models.TextField() 



class Event(models.Model):
    title = models.TextField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    organizer = models.ForeignKey(to="users.CustomUser", on_delete=models.CASCADE)
    privacy = models.ForeignKey(Privacy, on_delete=models.CASCADE)
    medium = models.ForeignKey(Medium, on_delete=models.CASCADE)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    duration = models.FloatField()
    language = models.CharField(max_length=255)
    locationName = models.TextField()
    latitude = models.TextField()
    longitude = models.TextField()
    acceptingRsvps = models.BooleanField()
    image = models.ImageField()
    members = models.IntegerField(default=0)
    maxParticipants = models.IntegerField()
    


class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user =  models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=True)


class Invitation(models.Model):
    evnet = models.ForeignKey(Event, on_delete=models.CASCADE)
    host = models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE, related_name='host')
    guest = models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE, related_name='guest')
    rsvp = models.ForeignKey(RSVP, on_delete=models.CASCADE)
