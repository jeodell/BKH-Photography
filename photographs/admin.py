from django.contrib import admin

from .models import Album, Photograph


class PhotographAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_added', 'img', 'album')
    list_display_links = ('id',)
    list_filter = ('album',)
    search_fields = ('album',)
    list_per_page = 25


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'cover')
    list_display_links = ('title',)
    search_fields = ('title',)
    list_per_page = 25


admin.site.register(Photograph, PhotographAdmin)
admin.site.register(Album, AlbumAdmin)
