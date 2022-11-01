from django.urls import path
from account.views import SendPasswordResetEmailView, UserChangePasswordView, UserProfileView, UserRegistrationView, UserLoginView
from . import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signup/register/', UserRegistrationView.as_view(), name='register'),
    # path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('login/done/', UserLoginView.as_view(), name='logindone'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('passwordchange/', UserChangePasswordView.as_view(), name='passwordchange'),
    path('sendresetpasswordemail/', SendPasswordResetEmailView.as_view(), name='sendresetpasswordemail'),
]
