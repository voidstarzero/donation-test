from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.contrib.auth.decorators import login_required
from django.db.models import Sum

from datetime import datetime

from .models import Club, Event, Attendee
from .utils import login_forbidden, do_donate

# Views are all preliminary until templates are refined

def index(request):
    now = datetime.now()
    context = {
            'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
            'current_events': (Event.objects.filter(start_time__lte=now)
                                            .filter(end_time__gte=now)
                                            .order_by('start_time')),
            'upcoming_events': (Event.objects.filter(start_time__gte=now)
                                             .order_by('start_time'))[:5],
            'attendees': Attendee.objects.all().order_by('-balance__cumulative')[:3],
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'clubs': Club.objects.all(),
    }
    return render(request, 'about.html', context)

def leaderboard_overview(request):
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'attendees': Attendee.objects.all().order_by('-balance__cumulative')[:3],
        'events': Event.objects.all().order_by('-balance__balance')[:5],
        'clubs': Club.objects.all().order_by('-balance__balance')[:3],
    }
    return render(request, 'leaderboards/index.html', context)

def leaderboard_by_attendee(request):
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'attendees': Attendee.objects.all().order_by('-balance__cumulative'),
    }
    return render(request, 'leaderboards/by_attendee.html', context)

def leaderboard_by_event(request):
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'events': Event.objects.all().order_by('-balance__balance'),
    }
    return render(request, 'leaderboards/by_event.html', context)

def leaderboard_by_club(request):
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'clubs': Club.objects.all().order_by('-balance__balance'),
    }
    return render(request, 'leaderboards/by_club.html', context)

def event_list(request):
    now = datetime.now()
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'current_events': (Event.objects.filter(start_time__lte=now)
                                        .filter(end_time__gte=now)
                                        .order_by('start_time')),
        'upcoming_events': (Event.objects.filter(start_time__gte=now)
                                         .order_by('start_time')),
        'past_events': (Event.objects.filter(end_time__lte=now)
                                     .order_by('start_time')),
        'events': Event.objects.all(),
    }
    return render(request, 'event_list.html', context)

def event_details(request, event):
    try:
        context = {
            'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
            'event': Event.objects.get(ref_name=event),
        }
        return render(request, 'event_details.html', context)

    except ObjectDoesNotExist:
        raise Http404('Event does not exist')

def club_details(request, club):
    try:
        context = {
            'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
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
            'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
            'events': Event.objects.all(),
            'selected': request.GET.get('event'),
        }
        return render(request, 'donate.html', context)

@login_required(login_url='/attendee/login')
def pay(request):
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
    }
    return render(request, 'pay.html', context)

@login_required(login_url='/attendee/login')
def change_password(request):
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
    }
    return render(request, 'attendee/change_password.html', context)

@login_forbidden(redirect_to='/attendee/logout')
def create_attendee(request):
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
    }
    return render(request, 'attendee/create.html', context)

@login_forbidden(redirect_to='/attendee/logout')
def login(request):
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
    }
    return render(request, 'attendee/login.html', context)

@login_required(login_url='/attendee/login')
def logout(request):
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
    }
    return render(request, 'attendee/logout.html', context)

@login_required(login_url='/attendee/login')
def attendee_profile(request):
    context = {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'attendee': Attendee.objects.get(user=request.user.id),
    }
    return render(request, 'attendee/profile.html', context)
