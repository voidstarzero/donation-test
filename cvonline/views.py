from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist

from .models import Club, Event

# Views are all preliminary until templates are refined

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def leaderboard_overview(request):
    return render(request, 'leaderboards/index.html')

def leaderboard_by_attendee(request):
    return render(request, 'leaderboards/by_attendee.html')

def leaderboard_by_event(request):
    return render(request, 'leaderboards/by_event.html')

def leaderboard_by_club(request):
    return render(request, 'leaderboards/by_club.html')

def event_list(request):
    return render(request, 'events/list.html')

def event_details(request, event):
    try:
        context = {
            'event': Event.objects.get(ref_name=event),
        }
        return render(request, 'event_details.html', context)

    except ObjectDoesNotExist:
        raise Http404('Event does not exist')

def club_details(request, club):
    try:
        context = {
            'club': Club.objects.get(ref_name=club),
        }
        return render(request, 'club.html', context)

    except ObjectDoesNotExist:
        raise Http404('Club does not exist')

def donate(request):
    return render(request, 'donate.html')

def pay(request):
    return render(request, 'pay.html')
