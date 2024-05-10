from django.shortcuts import render, redirect
from apps.posts.models.post import Post
from django.db.models import Q
import re


def home(request):
    context = {"posts": Post.objects.filter(is_published=True)}
    return render(request, "layouts/home.html", context)


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
