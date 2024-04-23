from django.db import models
from django.contrib.auth import get_user_model  # Get the custom user model


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return self.user.username
