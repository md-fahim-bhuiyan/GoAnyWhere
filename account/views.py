from urllib import request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from account.serializers import  UserRegistrationserializer
from account.renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from .models import Destination
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
def home(request):
    return render(request, 'home.html')

class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationserializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return render(request, 'home.html')
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

def register(request):
    return render(request, 'registation.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, 'Sucessfully Logged in')
            email = request.user.email
            print(email)
            content = 'Hello ' + request.user.name + '\n' + 'You are logged in in our site.keep connected and keep travelling.'
            dests = Destination.objects.all()
            return render(request, 'home.html',{'dests':dests})
        else:
            messages.info(request, 'Invalid credential')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')
