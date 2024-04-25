from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)  # Optional phone number
    birthday = models.DateField(null=True, blank=True)  # Optional date of birth
    profile_image = models.ImageField(upload_to="profile_images/", blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="following_profiles",
        blank=True,
    )

    def __str__(self):
        return self.user.username
