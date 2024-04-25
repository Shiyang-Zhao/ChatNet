from django.db import models
from django.conf import settings
from django.utils import timezone


class Chat(models.Model):
    PRIVATE = "private"
    GROUP = "group"
    CHAT_TYPES = [
        (PRIVATE, "Private"),
        (GROUP, "Group"),
    ]

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="chats"
    )
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPES, default=PRIVATE)
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="chat_images/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_chats",
    )

    def __str__(self):
        return f"{self.title} ({self.chat_type})"
