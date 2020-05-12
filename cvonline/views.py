from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.contrib.auth.decorators import login_required

from .models import Club, Event
from .utils import do_donate

# Views are all preliminary until templates are refined

def index(request):
    return render(request, 'index.html')

def about(request):
    context = {
        'clubs': Club.objects.all(),
    }
    return render(request, 'about.html', context)

def leaderboard_overview(request):
    return render(request, 'leaderboards/index.html')

def leaderboard_by_attendee(request):
    return render(request, 'leaderboards/by_attendee.html')

def leaderboard_by_event(request):
    return render(request, 'leaderboards/by_event.html')

def leaderboard_by_club(request):
    return render(request, 'leaderboards/by_club.html')

def event_list(request):
    context = {
        'events': Event.objects.all(),
    }
    return render(request, 'event_list.html', context)

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

@login_required(login_url='/attendee/login')
def donate(request):
    if request.method == 'POST':
        try:
            event_ref = request.POST['event']
            amount = request.POST['amount']
            do_donate(request.user.attendee_info.user, event_ref, amount)
            return HttpResponseRedirect('/')

        except (KeyError, ValueError):
            raise SuspiciousOperation('Wrong parameters to donate')

    elif request.method == 'GET':
        context = {
            'events': Event.objects.all(),
            'selected': request.GET.get('event'),
        }
        return render(request, 'donate.html', context)

@login_required(login_url='attendee/login')
def pay(request):
    return render(request, 'pay.html')
