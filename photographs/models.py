from django.db import models
from django.shortcuts import reverse


class Album(models.Model):
    title = models.CharField(max_length=100)
    cover = models.FileField(blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('album', kwargs={
            'album': self.title
        })

    class Meta:
        ordering = ['title']


class Photograph(models.Model):
    description = models.TextField(blank=True)
    img = models.ImageField(upload_to='images/portfolio')
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['date_added']
