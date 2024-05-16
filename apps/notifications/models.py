from django.db import models
from django.utils import timezone
from django.conf import settings


class Notification(models.Model):
    MESSAGE = "message"
    FRIEND_REQUEST = "friend_request"
    SYSTEM_ALERT = "system_alert"
    EVENT_REMINDER = "event_reminder"
    NOTIFICATION_TYPES = [
        (MESSAGE, "Message"),
        (FRIEND_REQUEST, "Friend Request"),
        (SYSTEM_ALERT, "System Alert"),
        (EVENT_REMINDER, "Event Reminder"),
    ]
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="sent_notifications",
    )
    notification_type = models.CharField(max_length=15, choices=NOTIFICATION_TYPES)
    content = models.TextField(default="You have a new notification.")
    date_sent = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification({self.notification_type}) for {self.recipient.username}"
