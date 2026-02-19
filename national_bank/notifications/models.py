from django.db import models
from django.conf import settings
from django.utils import timezone


class Notification(models.Model):
    TYPE_SYSTEM = 'system'
    TYPE_USER = 'user'
    TYPE_CHOICES = [
        (TYPE_SYSTEM, 'System'),
        (TYPE_USER, 'User'),
    ]

    PRIORITY_HIGH = 'high'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_LOW = 'low'
    PRIORITY_CHOICES = [
        (PRIORITY_HIGH, 'High'),
        (PRIORITY_MEDIUM, 'Medium'),
        (PRIORITY_LOW, 'Low'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    notification_type = models.CharField(max_length=16, choices=TYPE_CHOICES, default=TYPE_SYSTEM)
    target_user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE, related_name='notifications')
    is_read = models.BooleanField(default=False, db_index=True)
    priority = models.CharField(max_length=16, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM, db_index=True)
    send_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['target_user', 'is_read']),
            models.Index(fields=['notification_type']),
            models.Index(fields=['priority']),
        ]

    def __str__(self):
        target = self.target_user.username if self.target_user else 'All Users'
        return f"[{self.priority}] {self.title} -> {target}"

    def mark_read(self):
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read', 'updated_at'])

    def is_scheduled(self):
        return self.send_at is not None and self.send_at > timezone.now()
