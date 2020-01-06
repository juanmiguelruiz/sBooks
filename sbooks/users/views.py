from django.conf import settings
from django.contrib.auth.views import LoginView, logout
from django.shortcuts import render, redirect
# Create your views here.

class LoginUser(LoginView):
    template_name = 'login.html'

def LogoutUser(request):
    logout(request)
    return redirect('/index')

def login(request):
    return render(request, 'login.html', {'STATIC_URL': settings.STATIC_URL})



