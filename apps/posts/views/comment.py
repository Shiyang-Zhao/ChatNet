from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, View
from ..models.comment import Comment
from ..models.post import Post
from ..forms.comment import (
    CommentCreateForm,
    ReplyCreateForm,
    CommentUpdateForm,
    ReplyUpdateForm,
)
from django.http import JsonResponse


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = "posts/post_detail.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = ReplyCreateForm
    template_name = "posts/post_detail.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        parent_comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        form.instance.parent_comment = parent_comment
        form.instance.post = parent_comment.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentUpdateForm
    template_name = "comments/comment_update.html"

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class ReplyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = ReplyUpdateForm
    template_name = "comments/reply_update.html"

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "comment/delete_comment.html"

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if comment.author != self.request.user:
            pass
        return comment


class LikeCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        user = request.user
        like_status = 0
        if user in comment.liked_by.all():
            comment.liked_by.remove(user)
        else:
            comment.like(user.pk)
            like_status = 1
        return JsonResponse(
            {
                "success": True,
                "likes_count": comment.liked_by.count(),
                "dislikes_count": comment.disliked_by.count(),
                "like_status": like_status,
            }
        )


class DislikeCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        user = request.user
        like_status = 0
        if user in comment.disliked_by.all():
            comment.disliked_by.remove(user)
        else:
            comment.dislike(user.pk)
            like_status = -1
        return JsonResponse(
            {
                "success": True,
                "likes_count": comment.liked_by.count(),
                "dislikes_count": comment.disliked_by.count(),
                "like_status": like_status,
            }
        )
