from django.db import models
from django.contrib.auth.models import User


class VoiceInputLog(models.Model):
    """
    Log all voice input entries for analytics and debugging
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transcript = models.TextField()
    parsed_data = models.JSONField()
    confidence = models.FloatField(default=0.8)
    was_saved = models.BooleanField(default=False)
    expense_id = models.IntegerField(null=True, blank=True)
    income_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Voice Input Log'
        verbose_name_plural = 'Voice Input Logs'
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.transcript[:50]} ({self.created_at.strftime('%Y-%m-%d %H:%M')})"


class VoiceCommand(models.Model):
    """
    Store custom voice commands for users
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    command = models.CharField(max_length=100)
    description = models.TextField()
    example = models.CharField(max_length=200)
    category = models.CharField(max_length=50, default='expense')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['command']
        verbose_name = 'Voice Command'
        verbose_name_plural = 'Voice Commands'
    
    def __str__(self):
        return f"{self.command} - {self.user.username}"
