"""donation_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from cvonline import views

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('leaderboards/', views.leaderboard_overview, name='leaderboard'),
    path('leaderboards/by_attendee', views.leaderboard_by_attendee, name='leaderboard_by_attendee'),
    path('leaderboards/by_event', views.leaderboard_by_event, name='leaderboard_by_event'),
    path('leaderboards/by_club', views.leaderboard_by_club, name='leaderboard_by_club'),
    path('events/list', views.event_list, name='event_list'),
    path('events/<str:event>', views.event_details, name='event_details'),
    path('clubs/<str:club>', views.club_details, name='club_details'),
    path('donate', views.donate, name='donate'),
    path('pay', views.pay, name='pay'),
    path('attendee/change_password', views.change_password, name='change_password'),
    path('attendee/create', views.create_attendee, name='create_attendee'),
    path('attendee/login', views.login, name='login'),
    path('attendee/logout', views.logout, name='logout'),
    path('attendee/profile', views.attendee_profile, name='attendee_profile'),
    path('attendee/reset_password', views.reset_password, name='reset_password'),
    path('admin/', admin.site.urls), # leave to allow access to prebuilt admin site
]
