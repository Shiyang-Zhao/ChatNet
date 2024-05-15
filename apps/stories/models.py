from django.db import models
from django.conf import settings
from django.utils import timezone


class Story(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stories"
    )
    content = models.ImageField(
        upload_to="stories/"
    )  # For simplicity, assuming only images.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Story by {self.user.username} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    @property
    def is_active(self):
        """Check if the story is still active. Stories are active for 24 hours."""
        return self.created_at >= timezone.now() - timezone.timedelta(hours=24)
