from django.shortcuts import render, redirect
from .models import Photograph, Album
from .forms import ContactForm
from django.views.generic import View, ListView, TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


class HomepageView(View):
    def get(self, request, *args, **kwargs):
        albums = Album.objects.all()
        form = ContactForm()

        context = {
            'albums': albums,
            'form': form
        }

        return render(request, "photographs/home.html", context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            recipients = [settings.EMAIL_HOST_USER, settings.JBUG_EMAIL]
            subject = f'New message from { name }'

            try:
                send_mail(subject, message, email, recipients)
                messages.success(request, 'Your message has been sent.')
            except:
                messages.warning(request, 'Your message could not be sent.')
            return redirect('homepage')
        else:
            messages.warning(request, 'Your form was not valid.')
            return redirect('homepage')


def get_album_view(request, album):
    if request.method == 'GET':
        photographs = Photograph.objects.filter(album__title=album)

        context = {
            'photographs': photographs
        }

        return render(request, 'photographs/album.html', context)
    return redirect('homepage')


class AboutView(TemplateView):
    def get(self, request, *args, **kwargs):
        form = ContactForm()

        context = {
            'form': form
        }

        return render(request, "photographs/about.html", context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            recipients = [settings.EMAIL_HOST_USER, settings.JBUG_EMAIL]
            subject = f'New message from { name }'

            try:
                send_mail(subject, message, email, recipients)
                messages.success(request, 'Your message has been sent.')
            except:
                messages.warning(request, 'Your message could not be sent.')
            return redirect('homepage')
        else:
            messages.warning(request, 'Your form was not valid.')
            return redirect('homepage')
