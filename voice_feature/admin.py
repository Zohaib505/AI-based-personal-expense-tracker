from django.contrib import admin
from .models import VoiceInputLog, VoiceCommand


@admin.register(VoiceInputLog)
class VoiceInputLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'transcript_short', 'confidence', 'was_saved', 'created_at']
    list_filter = ['was_saved', 'created_at', 'user']
    search_fields = ['transcript', 'user__username']
    readonly_fields = ['transcript', 'parsed_data', 'user', 'created_at']
    
    def transcript_short(self, obj):
        return obj.transcript[:50] + '...' if len(obj.transcript) > 50 else obj.transcript
    transcript_short.short_description = 'Transcript'


@admin.register(VoiceCommand)
class VoiceCommandAdmin(admin.ModelAdmin):
    list_display = ['command', 'user', 'category', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'user']
    search_fields = ['command', 'user__username', 'example']
    fieldsets = (
        ('Command Info', {
            'fields': ('command', 'description', 'example', 'category')
        }),
        ('Status', {
            'fields': ('user', 'is_active', 'created_at')
        }),
    )
    readonly_fields = ['created_at']
