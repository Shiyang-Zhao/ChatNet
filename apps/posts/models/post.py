from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
import os


class Post(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(null=True, blank=True, upload_to="Files")
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )

    liked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liked_posts", blank=True
    )
    disliked_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="disliked_posts", blank=True
    )
    comments_count = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    def like(self, user_pk):
        if not self.liked_by.filter(pk=user_pk).exists():
            self.liked_by.add(user_pk)
            self.disliked_by.remove(user_pk)

    def dislike(self, user_pk):
        if not self.disliked_by.filter(pk=user_pk).exists():
            self.disliked_by.add(user_pk)
            self.liked_by.remove(user_pk)
