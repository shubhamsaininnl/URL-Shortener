from django.db import models

from shortener.models import KirrUrl
from shortener.models import KirrUrl
# Create your models here.

class ClickManager(models.Manager):
    def create_event(self, instance):
        if isinstance(instance, KirrUrl):
            obj, created = self.get_or_create(kirr_url=instance)
            obj.count += 1
            obj.save()
            return obj.count
        return None

class Click(models.Model):
    kirr_url = models.OneToOneField(KirrUrl)
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ClickManager()

    def __str__(self):
        return "{}".format(self.kirr_url)