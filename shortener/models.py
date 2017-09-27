from django.db import models
from django.conf import settings
# from django.core.urlresolvers import reverse
from django_hosts.resolvers import reverse

from .utils import create_shortcode
from .validators import validate_com, validate_url

# Create your models here.
SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class KirrUrlManager(models.Manager):

    def all(self, *args, **kwargs):
        qs_main = super(KirrUrlManager, self).all(*args, **kwargs)
        qs = qs_main.filter(active=True)
        return qs

    def refresh_shortcodes(self):
        qs = KirrUrl.objects.filter(id__gte=1)
        refreshed = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            refreshed += 1
            q.save()
        return "{} Codes refreshed".format(refreshed)

class KirrUrl(models.Model):
    url = models.CharField(max_length=220,validators=[validate_url, validate_com])
    shortcode = models.CharField(max_length=SHORTCODE_MAX, unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    objects = KirrUrlManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == '':
            self.shortcode = create_shortcode(self)
        # if not "http" in self.url:
        #     self.url = "http://" + self.url
        super(KirrUrl, self).save(*args, **kwargs)

    def __str__(self):
        return self.url


    def get_absolute_url(self):
        url_path = reverse("shortcode", kwargs={'shortcode': self.shortcode}, host='www', scheme='http')
        # return "http://www.yashanshu.com:8000" + url_path
        return url_path