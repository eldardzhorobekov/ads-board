from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from user.forms import CustomUserCreationForm, CustomUserLoginForm
from django.conf import settings


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class LoginView(auth_views.LoginView):
    authentication_form = CustomUserLoginForm
    template_name = 'registration/login.html'