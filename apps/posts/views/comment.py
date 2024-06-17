from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, View
from ..models.comment import Comment
from ..models.post import Post
from ..forms.comment import (
    CommentCreateForm,
    ReplyCreateForm,
    CommentUpdateForm,
)
from django.http import JsonResponse
from django.utils import timezone


class CommentDetailView(DetailView):
    model = Comment
    template_name = "apps/posts/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = get_object_or_404(Post, pk=self.kwargs.get("post_pk"))
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm
    template_name = "apps/posts/post_detail.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        return super().form_valid(form)


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = ReplyCreateForm
    template_name = "apps/posts/post_detail.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        parent_comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        form.instance.parent_comment = parent_comment
        form.instance.post = parent_comment.post
        return super().form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentUpdateForm

    def form_valid(self, form):
        form.instance.edited = True
        form.instance.edited_at = timezone.now()
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentSoftDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    model = Comment

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get("pk"))
        if self.request.user == comment.author:
            comment.soft_delete()
        return redirect(reverse_lazy("post-detail", kwargs={"pk": comment.post.pk}))

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        return self.request.user == comment.author


class CommentHardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse("post-detail", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        return self.request.user == comment.author


class LikeCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        user = request.user
        like_status = 0
        if user in comment.liked_by.all():
            comment.liked_by.remove(user)
        else:
            comment.like_comment(user.pk)
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
            comment.dislike_comment(user.pk)
            like_status = -1
        return JsonResponse(
            {
                "success": True,
                "likes_count": comment.liked_by.count(),
                "dislikes_count": comment.disliked_by.count(),
                "like_status": like_status,
            }
        )


class SaveCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        comment.save_comment(request.user)
        return redirect("comment-detail", post_pk=comment.post.pk, pk=comment.pk)


class UnsaveCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        comment.unsave_comment(request.user)
        return redirect("comment-detail", post_pk=comment.post.pk, pk=comment.pk)
