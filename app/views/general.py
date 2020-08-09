from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import  auth, messages
from ..forms import *
from ..models import *
from django.contrib.auth import logout as django_logout
from difflib import SequenceMatcher
import datetime
from django.contrib.auth.decorators import login_required
import operator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView, TemplateView)
from django.db.models import Count
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.utils.decorators import method_decorator
from ..decorators import customer_required



class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    return render(request, 'general/home.html')

def FrontPage(request):
    template_name = 'frontpage/index.html'
    return render(request, template_name)


def login(request):

        if request.method == "POST":
            form = AuthenticationForm(request, data=request.POST)
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            if form.is_valid():
                user = auth.authenticate(username=username, password=password)

                if user is not None:
                    auth.login(request, user)

                    if request.user.is_customer:
                        return redirect('customer:dashboard')
                    elif request.user.is_bike:
                        return redirect('bike:dashboard')
                                                
            
            else:
                args = {'form': form}
                return render(request, 'registration/login.html', args)

        else:
            form = AuthenticationForm

        args = {'form': form}
        return render(request, 'registration/login.html', args)


def logout_user(request):
    django_logout(request)
    return redirect('userlogin')


