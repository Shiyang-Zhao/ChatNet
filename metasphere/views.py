from django.shortcuts import render
from apps.posts.models.post import Post


def home(request):
    # Retrieve all posts from the database
    posts = (
        Post.objects.all()
    )  # Or add filters like 'Post.objects.filter(published=True)'

    return render(request, "layouts/home.html", {"posts": posts})
