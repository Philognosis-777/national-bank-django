from django.contrib import admin
from .models import PaperNews, VideoNews, VerbalAnnouncement


@admin.register(PaperNews)
class PaperNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    search_fields = ('title', 'summary', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(VideoNews)
class VideoNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(VerbalAnnouncement)
class VerbalAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'announcement_date', 'is_published')
    search_fields = ('title', 'short_description', 'transcript')
    prepopulated_fields = {'slug': ('title',)}
