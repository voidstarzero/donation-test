from django.http import HttpResponse
from django.shortcuts import render

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
    return render(request, 'events/{}.html'.format(event))

def club_details(request, club):
    return render(request, 'clubs/{}.html'.format(club))

def donate(request):
    return render(request, 'donate.html')

def pay(request):
    return render(request, 'pay.html')
