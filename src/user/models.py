from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator

from phonenumber_field.modelfields import PhoneNumberField

from user.managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        null=True,
        blank=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
        blank=True,
        default=None,
        null=True,
        error_messages={
            'unique': _('A user with that email already exists.'),
        }
    )
    phone_number = PhoneNumberField(
        _('phone number'),
        unique=True,
        blank=True, 
        default=None,
        null=True,
        error_messages={
            'unique': _('A user with that phone number already exists.'),
        }
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        blank=True,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
        blank=True,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into '
            'this admin site.'
        ),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be '
            'treated as active. Unselect this instead '
            'of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    ordering = ('email',)

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.username or self.email or str(self.phone_number)
    
    def clean(self):
        if not self.email and not self.phone_number:
            raise ValidationError('You must provide either Email or Phone number')