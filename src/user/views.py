from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.conf import settings
from user.forms import CustomUserCreationForm, CustomUserLoginForm

CustomUser = get_user_model()

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/signup.html'


class LoginView(auth_views.LoginView):
    authentication_form = CustomUserLoginForm
    template_name = 'account/login.html'
    
class UserDetails(DetailView):
    model = CustomUser
    template_name = 'account/user-details.html'
    context_object_name = 'user_object'

    def get_context_data(self, **kwargs):
        context = super(UserDetails, self).get_context_data(**kwargs)
        context['test'] = "This is test string"

        return context