from django.db import models
from django.db.models import Count


class AdvertisementManager(models.Manager):
    def get_queryset_by_author(self, author):
        return super().get_queryset().filter(author=author)

    def with_counts(self):
        return self.annotate(
            images_count=Count('images')
        )