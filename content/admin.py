from django.contrib import admin
from .models import Page, VideoContent, AudioContent

class VideoContentInline(admin.TabularInline):
    model = VideoContent
    extra = 1

class AudioContentInline(admin.TabularInline):
    model = AudioContent
    extra = 1

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title__istartswith']
    inlines = [VideoContentInline, AudioContentInline]

@admin.register(VideoContent)
class VideoContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'counter']
    search_fields = ['title__istartswith']

@admin.register(AudioContent)
class AudioContentAdmin(admin.ModelAdmin):
    list_display = ['title', 'page', 'counter']
    search_fields = ['title__istartswith']