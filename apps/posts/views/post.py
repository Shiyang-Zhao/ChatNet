from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from ..models.post import Post
from ..forms.post import PostCreateForm, PostUpdateForm
from ..forms.comment import CommentCreateForm, ReplyCreateForm
from django.http import JsonResponse


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    ordering = ["-date_posted"]
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comment_create_form"] = CommentCreateForm()
        context["reply_create_form"] = ReplyCreateForm()
        context["parent_comments"] = post.comments.filter(parent_comment__isnull=True)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "posts/post_create_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = "posts/post_update_form.html"

    def get_object(self):
        return get_object_or_404(
            Post, pk=self.kwargs.get("pk"), author=self.request.user
        )

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"

    def get_object(self):
        return get_object_or_404(
            Post, pk=self.kwargs.get("pk"), author=self.request.user
        )

    def get_success_url(self):
        return reverse("home")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully.")
        return super().delete(request, *args, **kwargs)


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        user = request.user
        if user in post.liked_by.all():
            post.liked_by.remove(user)
        else:
            post.like(user.pk)
        return JsonResponse(
            {
                "success": True,
                "likes_count": post.liked_by.count(),
                "dislikes_count": post.disliked_by.count(),
            }
        )


class DislikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        user = request.user
        if user in post.disliked_by.all():
            post.disliked_by.remove(user)
        else:
            post.dislike(user.pk)
        return JsonResponse(
            {
                "success": True,
                "likes_count": post.liked_by.count(),
                "dislikes_count": post.disliked_by.count(),
            }
        )
