from django.contrib import admin
from .models.post import Post
from .models.comment import Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
