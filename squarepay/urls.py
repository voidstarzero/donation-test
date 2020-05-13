from django.urls import path

from . import views

app_name = 'squarepay'

urlpatterns = [
    path('', views.payment_form, name='payment'),
    path('process', views.process_payment, name='process'),
]
