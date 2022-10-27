from django.urls import path
from account.views import UserChangePasswordView, UserProfileView, UserRegistrationView, UserLoginView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    # path('signup/', views.signup, name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('passwordchange/', UserChangePasswordView.as_view(), name='passwordchange'),
]
