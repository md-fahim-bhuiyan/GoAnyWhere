from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('verify', views.verify, name='verify'),
    path('signin', views.signin, name='signin'),
]
