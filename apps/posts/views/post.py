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
from django.http import JsonResponse
from django.utils import timezone


class PostDetailView(DetailView):
    model = Post
    template_name = "apps/posts/post_detail.html"

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(
            Post, pk=kwargs.get("pk"), is_deleted=False, is_published=True
        )

        session_key = f"viewed_post_{self.object.pk}"
        if not request.session.get(session_key, False):
            self.object.views += 1
            self.object.save(update_fields=["views"])
            request.session[session_key] = True

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = "apps/posts/post_create_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostUpdateForm
    template_name = "apps/posts/post_update_form.html"

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
            post.like_post(user.pk)
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
            post.dislike_post(user.pk)
            like_status = -1
        return JsonResponse(
            {
                "success": True,
                "likes_count": post.liked_by.count(),
                "dislikes_count": post.disliked_by.count(),
                "like_status": like_status,
            }
        )


class SavePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        post.save_post(request.user)
        return redirect("post-detail", pk=post.pk)


class UnsavePostView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        post.unsave_post(request.user)
        return redirect("post-detail", pk=post.pk)
