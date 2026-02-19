from typing import Dict, Any, Optional
from django.utils import timezone
from django.db import transaction
from django.contrib.auth import get_user_model

from .models import Notification


def create_notification(title: str, content: str, notification_type: str = Notification.TYPE_SYSTEM,
                        target_user_id: Optional[int] = None, priority: str = Notification.PRIORITY_MEDIUM,
                        send_at: Optional[timezone.datetime] = None) -> Notification:
    """Create a notification. For system notifications, target_user_id should be None."""
    User = get_user_model()
    target_user = None
    if target_user_id:
        target_user = User.objects.filter(pk=target_user_id).first()

    with transaction.atomic():
        n = Notification.objects.create(
            title=title,
            content=content,
            notification_type=notification_type,
            target_user=target_user,
            priority=priority,
            send_at=send_at,
        )
    return n


def get_unread_notifications_for_user(user, limit: int = 50):
    """Efficiently return unread notifications for a user, including system notifications."""
    qs = Notification.objects.filter(
        models.Q(notification_type=Notification.TYPE_SYSTEM) | models.Q(target_user=user)
    ).order_by('-created_at')
    # unread first
    qs = qs.order_by('-is_read', '-created_at')
    return qs[:limit]


def mark_notification_read(notification: Notification):
    notification.mark_read()
    return notification


def get_scheduled_notifications(now: Optional[timezone.datetime] = None):
    now = now or timezone.now()
    return Notification.objects.filter(send_at__isnull=False, send_at__lte=now)
