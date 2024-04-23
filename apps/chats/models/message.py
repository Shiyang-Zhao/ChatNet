from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from .chat import Chat

User = get_user_model()


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    attachment = models.FileField(
        upload_to="message_attachments/", null=True, blank=True
    )

    def __str__(self):
        return f"Message {self.id} from {self.sender} in {self.chat}"
