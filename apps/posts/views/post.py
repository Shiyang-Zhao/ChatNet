from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from ..models.post import Post
from ..forms.post import PostCreateForm, PostUpdateForm
from ..forms.comment import CommentCreateForm, ReplyCreateForm
from django.http import JsonResponse
from django.utils import timezone


# class PostListView(ListView):
#     model = Post
#     template_name = "posts/post_list.html"
#     context_object_name = "posts"
#     ordering = ["-date_posted"]
#     paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comment_create_form"] = CommentCreateForm()
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


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = "posts/post_update_form.html"

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class PostSoftDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs.get("pk"))
        if self.request.user == post.author:
            post.is_deleted = True
            post.soft_deleted_at = timezone.now()
            post.save()
        return redirect(reverse_lazy("home"))

    def test_func(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        return self.request.user == post.author


class PostHardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy("home")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class LikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        user = request.user
        like_status = 0
        if user in post.liked_by.all():
            post.liked_by.remove(user)
        else:
            post.like(user.pk)
            like_status = 1
        return JsonResponse(
            {
                "success": True,
                "likes_count": post.liked_by.count(),
                "dislikes_count": post.disliked_by.count(),
                "like_status": like_status,
            }
        )


class DislikePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        user = request.user
        like_status = 0
        if user in post.disliked_by.all():
            post.disliked_by.remove(user)
        else:
            post.dislike(user.pk)
            like_status = -1
        return JsonResponse(
            {
                "success": True,
                "likes_count": post.liked_by.count(),
                "dislikes_count": post.disliked_by.count(),
                "like_status": like_status,
            }
        )
