from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from pathlib import Path
from django.utils.timezone import localtime


def post_file_directory_path(instance, filename):
    date_posted_str = localtime(instance.date_posted).strftime("%Y/%m/%d")
    return str(
        Path("files/posts") / instance.author.username / date_posted_str / filename
    )


class Post(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to=post_file_directory_path, null=True, blank=True)
    content = models.TextField(blank=True)
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
    saved_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="saved_posts", blank=True
    )
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)  # Soft delete field
    soft_deleted_at = models.DateTimeField(null=True, blank=True)

    @property
    def parent_comments(self):
        return self.comments.filter(parent_comment__isnull=True)

    @property
    def file_name(self):
        return Path(self.file.name).name
    @property
    def file_extension(self):
        return Path(self.file.name).suffix

    @classmethod
    def active_posts(cls, user):
        return cls.objects.filter(
            author=user,
            is_published=True,
            is_deleted=False,
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.pk})

    def like_post(self, user_pk):
        if not self.liked_by.filter(pk=user_pk).exists():
            self.liked_by.add(user_pk)
            self.disliked_by.remove(user_pk)

    def dislike_post(self, user_pk):
        if not self.disliked_by.filter(pk=user_pk).exists():
            self.disliked_by.add(user_pk)
            self.liked_by.remove(user_pk)

    def is_saved_by(self, user):
        return self.saved_by.filter(pk=user.pk).exists()

    def save_post(self, user):
        if not self.is_saved_by(user):
            self.saved_by.add(user)

    def unsave_post(self, user):
        if self.is_saved_by(user):
            self.saved_by.remove(user)

    def soft_delete(self):
        self.is_deleted = True
        self.soft_deleted_at = timezone.now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.soft_deleted_at = None
        self.save()
