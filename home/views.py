from importlib.resources import Resource
from urllib import response
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'registation.html')
