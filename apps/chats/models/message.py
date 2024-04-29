from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from .chat import Chat  # Make sure this import reflects your project structure


class Message(models.Model):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_messages",
    )
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    attachment = models.FileField(
        upload_to="message_attachments/", null=True, blank=True
    )

    def get_absolute_url(self):
        return reverse("chat-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return (
            f"Message from {self.sender} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
        )
