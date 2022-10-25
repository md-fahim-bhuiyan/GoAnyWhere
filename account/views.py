from django.shortcuts import render
from django.http import HttpResponse

def signup(request):
    return HttpResponse("SignUp!!")

def signin(request):
    return HttpResponse("Sign in!!")
    
def verify(request):
    return HttpResponse("verify in!!")