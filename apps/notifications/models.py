from django.db import models
from django.conf import settings


class Notification(models.Model):
    MESSAGE = "message"
    FRIEND_REQUEST = "friend_request"
    NOTIFICATION_TYPES = [
        (MESSAGE, "Message"),
        (FRIEND_REQUEST, "Friend Request"),
    ]

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications"
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="+"
    )
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    text = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification({self.type}) for {self.recipient.username}"
