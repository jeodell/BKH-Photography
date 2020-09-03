from django.shortcuts import render, redirect
from .models import Photograph, Album
from .forms import ContactForm
from django.views.generic import View, ListView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


class HomepageView(View):
    def get(self, request, *args, **kwargs):
        photographs = Photograph.objects.all()
        form = ContactForm()

        context = {
            'photographs': photographs,
            'form': form
        }

        return render(request, "photographs/home.html", context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            recipient = [settings.EMAIL_HOST_USER]
            subject = f'New message from { name }'

            try:
                send_mail(subject, message, email, recipient)
                messages.success(request, 'Your message has been sent.')
            except:
                messages.warning(request, 'Your message could not be sent.')
            return redirect('homepage')
        else:
            messages.warning(request, 'Your form was not valid.')
            return redirect('homepage')


class AlbumsView(ListView):
    model = Album
    template_name = 'photographs/albums.html'


def get_album_view(request, album):
    if request.method == 'GET':
        photographs = Photograph.objects.filter(album__title=album)

        context = {
            'photographs': photographs
        }

        return render(request, 'photographs/album.html', context)
    return redirect('homepage')
