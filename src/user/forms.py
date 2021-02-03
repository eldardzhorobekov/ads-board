from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from .helpers import *


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None:
            return email
        number_occurrences = User.objects.filter(email__iexact=email).count()
        if  number_occurrences > 0:
            raise forms.ValidationError("This email is already taken by another user")
        return email
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number is None:
            return None
        number_occurrences = User.objects.filter(phone_number=phone_number).count()
        if  number_occurrences > 0:
            raise forms.ValidationError("This phone number is already taken by another user")
        return phone_number

    def clean(self):
        if self.cleaned_data.get('email') is None and self.cleaned_data.get('phone_number') is None:
            raise forms.ValidationError("Either email or phone number must be set")
        return self.cleaned_data
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'phone_number', 'password1', 'password2')
        labels = {
            'email': 'Email',
            'phone_number': 'Номер телефона'
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('phone_number',)


class CustomUserLoginForm(AuthenticationForm):
    pass