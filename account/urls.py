from django.urls import path
from account.views import UserRegistrationView
from . import views
urlpatterns = [
    # path('register', views.register, name='register'),
    
    # # path('signup/', views.signup, name='signup'),
    # path('login', views.login, name='login'),
    # path('login/view/', UserLoginView.as_view(), name='loginview'),
    # path('profile/', UserProfileView.as_view(), name='profile'),
    # path('newpassword/passwordchange/', UserChangePasswordView.as_view(), name='passwordchange'),
    # path('sendresetpasswordemail/', SendPasswordResetEmailView.as_view(), name='sendresetpasswordemail'),
    # path('logout/', UserLogoutView.as_view(), name='logout'),
    # path('profileview/', views.profileview, name='profileview'),
    # path('newpassword/', views.newpassword, name='newpassword'),
    path('', views.home, name='home'),    
    path('register/', views.register, name='register'),
    path('register/done', UserRegistrationView.as_view(), name='registerdone'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
