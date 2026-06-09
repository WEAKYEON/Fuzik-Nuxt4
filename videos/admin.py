from django.contrib import admin
from .models import Video, JamSession

admin.site.register(Video)

@admin.register(JamSession)
class JamSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'layout')
    
    readonly_fields = ('id',)