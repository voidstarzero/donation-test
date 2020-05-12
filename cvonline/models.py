from django.db import models
from django.contrib import auth

User = auth.get_user_model()

class Club(models.Model):
    ref_name    = models.CharField(primary_key=True, max_length=15, blank=False, null=False)
    full_name   = models.CharField(max_length=120, null=False)
    page_link   = models.CharField(max_length=120, blank=False)
    description = models.TextField(null=False)

    def __str__(self):
        return self.full_name

# Holds extra information not stored in the User model
class Attendee(models.Model):
    user    = models.OneToOneField(User, primary_key=True, related_name='attendee_info', on_delete=models.CASCADE)
    clubs   = models.ManyToManyField(Club, related_name='members')

    def __str__(self):
        user = self.user
        return '{} ({} {})'.format(user.username, user.first_name, user.last_name)

class Event(models.Model):
    ref_name    = models.CharField(primary_key=True, max_length=15, blank=False, null=False)
    full_name   = models.CharField(max_length=120, null=False)
    start_time  = models.DateTimeField(null=False)
    end_time    = models.DateTimeField(null=True) # if event end is null, it's consider to be 'all day'
    page_link   = models.CharField(max_length=120, blank=True)
    description = models.TextField(null=False, blank=True)
    organizers  = models.ManyToManyField(Club, related_name='events')

    def __str__(self):
        return self.full_name

# From Attendees, to Events
class Donation(models.Model):
    amount          = models.IntegerField(null=False, blank=False)
    attendee_from   = models.ForeignKey(Attendee, on_delete=models.SET_NULL, related_name='donations', null=True)
    event_to        = models.ForeignKey(Event, on_delete=models.SET_NULL, related_name='donations', null=True)
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        attendee = self.attendee_from
        event = self.event_to
        return '{} to {} (${})'.format(attendee.user.username, event.full_name, self.amount)
