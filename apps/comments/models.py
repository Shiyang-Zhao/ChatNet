from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies"
    )
    likes = models.IntegerField(default=0)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    attachments = models.FileField(
        upload_to="comment_attachments/", null=True, blank=True
    )
    visibility = models.BooleanField(default=True)
    report_count = models.IntegerField(default=0)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.date_posted.strftime("%Y-%m-%d %H:%M")}'

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("comment-detail", kwargs={"pk": self.pk})

    @property
    def is_parent(self):
        return self.parent_comment is None

    @property
    def children(self):
        return Comment.objects.filter(parent_comment=self)
