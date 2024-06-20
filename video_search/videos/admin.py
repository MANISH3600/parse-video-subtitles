from django.contrib import admin
from .models import Subtitle,Video
# Register your models here.



class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')

class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'video_id', 'start_time', 'end_time', 'text')
    list_display_links = ('id',)

admin.site.register(Video, VideoAdmin)
admin.site.register(Subtitle, SubtitleAdmin)