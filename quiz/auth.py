from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
from django.contrib.auth import login, logout, authenticate, get_user_model

# define the custom user model
User = get_user_model()

def login_view(request):
    pass

def logout_view(request):
    pass