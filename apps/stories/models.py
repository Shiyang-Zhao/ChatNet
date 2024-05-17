from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import localtime
import datetime
from pathlib import Path


def story_file_directory_path(instance, filename):
    date_posted_str = localtime(instance.date_posted).strftime("%Y/%m/%d")
    return str(
        Path("files/stories") / instance.author.username / date_posted_str / filename
    )


def default_expiration_date():
    return timezone.now() + datetime.timedelta(hours=24)


class Story(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="stories"
    )
    file = models.FileField(upload_to=story_file_directory_path, null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    date_expired = models.DateTimeField(default=default_expiration_date)
    viewed_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="viewed_stories", blank=True
    )
    content = models.TextField(blank=True, null=True)
    is_archived = models.BooleanField(default=False)

    @property
    def is_expired(self):
        """Check if the story has expired (either by reaching its expiration date or being archived)."""
        return timezone.now() >= self.date_expired or self.is_archived

    @property
    def file_extension(self):
        return Path(self.file.name).suffix

    def __str__(self):
        return f"{self.user.username}'s Story at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def archive(self):
        """Archive the story. This function will change its archival status."""
        self.is_archived = True
        self.save()

    @classmethod
    def active_stories(cls, user):
        """Return active stories for a given user."""
        return cls.objects.filter(
            author=user, is_archived=False, date_expired__gt=timezone.now()
        )
