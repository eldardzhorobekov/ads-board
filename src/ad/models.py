from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator
from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.urls import reverse
from django.db import transaction

from mptt.models import MPTTModel, TreeForeignKey
from phonenumber_field.modelfields import PhoneNumberField

from ad.helpers import slugify
from ad.managers import AdvertisementManager


CustomUser = get_user_model()


class Category(MPTTModel):
    title = models.CharField(max_length=255, blank=True, null=True, default=None)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', default=0)
    icon = models.ImageField(upload_to='categories', blank=True, null=True)
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ('title', )
        verbose_name_plural = 'Categories'


class City(models.Model):
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.city

    class Meta:
        verbose_name_plural = 'Cities'

def upload_image_path(instance, filename):
    user_id = 0
    if isinstance(instance, Advertisement):
        user_id = instance.author.id
    elif isinstance(instance, AdvertisementImage):
        user_id = instance.advertisement.author.id
    return f"images/user_{user_id}/gallery/{filename}"

class Advertisement(models.Model):

    class Currency(models.TextChoices):
        SOM = 'SOM', _('SOM')
        USD = 'USD', _('USD')

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', _('ACTIVE')
        INACTIVE = 'INACTIVE', _('INACTIVE')
        IN_MODERATION = 'MODERATION', _('MODERATION')
        DECLINED = 'DECLINED', _('DECLINED')

    description = models.TextField(_('description'))
    price = models.IntegerField(
        _('price'),
        default=0,
    )
    currency = models.CharField(
        max_length=3,
        choices=Currency.choices,
        default=Currency.SOM
    )
    phone_number = PhoneNumberField(_('phone number'))
    hide_phone_number = models.BooleanField(
        _('hide phone number'),
        default=False)
    email = models.EmailField(
        _('email address'),
        unique=False,
        blank=True,
        default=None,
        null=True
    )
    category = TreeForeignKey (
        to=Category,
        on_delete=models.CASCADE,
        related_name='ads'
    )
    city = models.ForeignKey(
        to=City,
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        to=CustomUser,
        verbose_name=_('author'),
        on_delete=models.CASCADE,
        related_name='ads'
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    likes = models.ManyToManyField(CustomUser, related_name='liked_ads', blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_MODERATION

    )

    objects = AdvertisementManager()
    
    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('ads:ads-details', kwargs={'pk':self.pk})


class AdvertisementImage(models.Model):
    image = models.ImageField(upload_to=upload_image_path, blank=False, null=False)
    is_main = models.BooleanField(default=False)
    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name="images")

    def __str__(self):
        return self.image.name