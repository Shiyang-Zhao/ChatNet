from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.posts.models.post import Post
from apps.users.models.user import User
from apps.posts.models.comment import Comment
from apps.stories.models import Story
from django.db.models import Q
from django.utils import timezone
from django.db.models import Count
import re


def home(request):
    user = request.user
    context = {
        "active_posts": Post.objects.filter(
            is_published=True, is_deleted=False
        ).order_by("-date_posted")
    }
    if user.is_authenticated:
        active_authors = set()
        if Story.active_stories(user).exists():
            active_authors.add(user)
        for followed_user in user.profile.following.all():
            if Story.active_stories(followed_user.user).exists():
                active_authors.add(followed_user.user)
        context["active_authors"] = active_authors

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

    # Search in Posts
    posts = Post.objects.filter(
        Q(title__icontains=query)
        | Q(content__icontains=query)
        | Q(author__username__icontains=query),
        is_published=True,
    ).distinct()

    users = User.objects.filter(username__icontains=query).distinct()

    comments = Comment.objects.filter(
        Q(content__icontains=query) | Q(author__username__icontains=query)
    ).distinct()

    return render(
        request,
        "layouts/search_results.html",
        {
            "result_posts": posts,
            "result_users": users,
            "result_comments": comments,
            "query": query,
        },
    )


def sort(request):
    # Define the base query for posts
    base_query = Post.objects.filter(is_published=True, is_deleted=False)

    # Define the sort options and their corresponding query annotations and orders
    sort_options = {
        "new": ("New", "-date_posted"),
        "controversial": (
            "Controversial",
            "comment_count",
            Count("comments"),
            "-comment_count",
            "-date_posted",
        ),
        "old": ("Old", "date_posted"),
        "top": (
            "Top",
            "net_likes",
            Count("liked_by", distinct=True) - Count("disliked_by", distinct=True),
            "-net_likes",
            "-date_posted",
        ),
    }

    # Get the sorting method from the request, default to 'new'
    sort_method = request.GET.get("sort", "new")
    sort_method = sort_method if sort_method in sort_options else "new"

    # Prepare query based on the selected sort option
    sort_params = sort_options[sort_method]
    if sort_method in ["controversial", "top"]:
        # Annotate and order by the annotation
        active_posts = base_query.annotate(**{sort_params[1]: sort_params[2]}).order_by(
            sort_params[3], sort_params[4]
        )
    else:
        # No annotation needed, just order by the provided fields
        active_posts = base_query.order_by(sort_params[1])

    context = {
        "active_posts": active_posts,
        "sort_options": {key: val[0] for key, val in sort_options.items()},
    }

    return render(request, "layouts/home.html", context)


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
