from django.db import models
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError
from django.db import transaction
from django.core.cache import cache


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birthday = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_images/", blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    following = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="followers"
    )

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        raise PermissionDenied("Profiles cannot be deleted manually.")

    def follow(self, profile):
        if self == profile:
            raise ValidationError("You cannot follow yourself.")
        if self.is_following(profile):
            raise ValidationError("You are already following this profile.")

        self.following.add(profile)
        cache_key = f"following:{self.pk}:{profile.pk}"
        cache.set(cache_key, True)

    def unfollow(self, profile):
        if self == profile:
            raise ValidationError("You cannot unfollow yourself.")
        if not self.is_following(profile):
            raise ValidationError("You are not following this profile.")

        self.following.remove(profile)
        cache_key = f"following:{self.pk}:{profile.pk}"
        cache.set(cache_key, False)

    def is_following(self, profile):
        cache_key = f"following:{self.pk}:{profile.pk}"
        is_following = cache.get(cache_key)
        if is_following is None:
            is_following = self.following.filter(pk=profile.pk).exists()
            cache.set(cache_key, is_following)
        return is_following
