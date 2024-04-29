from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


class Chat(models.Model):
    PRIVATE = "private"
    GROUP = "group"
    CHAT_TYPES = [
        (PRIVATE, "Private"),
        (GROUP, "Group"),
    ]

    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="joined_chats",
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_chats",
    )
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPES, default=PRIVATE)
    created_at = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=255, default="default title")
    description = models.TextField(blank=True, default="description")
    image = models.ImageField(upload_to="chat_images/", null=True, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.chat_type})"

    def get_absolute_url(self):
        return reverse("chat-detail", kwargs={"pk": self.pk})

    @classmethod
    def get_existing_private_chat(cls, user1, user2):
        return (
            cls.objects.filter(
                chat_type=cls.PRIVATE,
                participants=user1,
            )
            .filter(participants=user2)
            .first()
        )
