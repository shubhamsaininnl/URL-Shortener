from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views import View

from .models import KirrUrl
from analytics.models import Click
from .forms import SubmitUrlForm
# Create your views here.

class HomeView(View):

    def get(self, request, *args, **kwargs):
        form = SubmitUrlForm()
        bg_image = "https://cdn.wallpapersafari.com/99/48/qyuSTK.jpg"
        context = {
            "title": "Submit URL Form",
            "form": form,
            "bg_image": bg_image
        }
        return render(request,'shortener/home.html' , context)

    def post(self, request, *args, **kwargs):
        form = SubmitUrlForm(request.POST)
        context = {
            "title": "Done",
            "form": form
        }
        template = "shortener/home.html"
        if form.is_valid():
            new_url = form.cleaned_data['url']
            obj, created = KirrUrl.objects.get_or_create(url=new_url)
            context = {
                "object": obj,
                "created": created
            }
            if created:
                template = "shortener/success.html"
            else:
                template = "shortener/already-exists.html"
        return render(request, template, context)

class Kirr(View):
    def get(self, request,shortcode=None, *args, **kwargs):
        obj = get_object_or_404(KirrUrl, shortcode=shortcode)
        qs = KirrUrl.objects.filter(shortcode__iexact=shortcode)
        if qs.count() != 1 and not qs.exists():
            raise Http404
        print(Click.objects.create_event(obj))
        return HttpResponseRedirect(obj.url)