from django.urls import path
from .models import Destination
from . import views
urlpatterns = [
    path('flight', views.flight, name='flight')
]