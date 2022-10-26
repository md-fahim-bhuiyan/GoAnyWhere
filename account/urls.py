from django.urls import path
from account.views import UserRegistrationView
urlpatterns = [
    path('signup/', UserRegistrationView.as_view(), name='signup'),
]
