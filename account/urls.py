from django.urls import path
from account.views import UserRegistrationView
from . import views
urlpatterns = [
    path('', views.home, name='home'),    
    path('register/', views.register, name='register'),
    path('register/done', UserRegistrationView.as_view(), name='registerdone'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
