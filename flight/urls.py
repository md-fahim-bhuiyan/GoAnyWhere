from django.urls import path
from .models import Destination
from . import views
urlpatterns = [
    path('search', views.search, name='search'),
    path('destination_list/<str:city_name>', views.destination_list, name='destination_list'),
    path('destination_list/destination_details/<str:city_name>', views.destination_details, name='destination_details'),
    path('destination_details/<str:city_name>', views.destination_details, name='destination_details'),
    path('destination_list/destination_details/pessanger_detail_def/<str:city_name>',views.pessanger_detail_def,name='pessanger_detail_def'),
    path('upcoming_trips', views.upcoming_trips, name='upcoming_trips'),
]