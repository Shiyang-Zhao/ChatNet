from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.posts.models.post import Post
from apps.stories.models import Story
from django.db.models import Q
from django.utils import timezone
import re


def home(request):
    context = {"active_posts": Post.objects.filter(is_published=True, is_deleted=False)}
    return render(request, "layouts/home.html", context)


@login_required
def search(request):
    query = request.GET.get("q", "")
    if query.isspace():
        query = " "
    else:
        query = re.sub(r"\s+", " ", query).strip()

    if not query:
        return redirect("home")

    results = Post.objects.filter(
        Q(title__icontains=query)
        | Q(content__icontains=query)
        | Q(author__username__icontains=query),
        is_published=True,
    ).distinct()

    return render(
        request, "posts/search_results.html", {"results": results, "query": query}
    )


@login_required
def setting(request):
    return render(request, "layouts/setting.html")


@login_required
def history(request):
    context = {
        "deleted_posts": Post.objects.filter(
            author=request.user, is_published=True, is_deleted=True
        ),
        "archived_stories": Story.objects.filter(author=request.user, is_archived=True),
        "expired_stories": Story.objects.filter(
            author=request.user,
            is_archived=False,
            date_expired__lt=timezone.now(),
        ),
    }
    return render(request, "layouts/history.html", context)
