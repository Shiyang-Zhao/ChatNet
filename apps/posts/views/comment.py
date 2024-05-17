from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView, View
from ..models.comment import Comment
from ..models.post import Post
from ..forms.comment import CommentCreateForm, ReplyCreateForm
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


##################### UserPassesTestMixin ######################

# class CommentUpdateView(LoginRequiredMixin, UpdateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = "comment/edit_comment_form.html"

#     def get_object(self, queryset=None):
#         comment = super().get_object(queryset)
#         if comment.author != self.request.user:
#             pass
#         return comment

#     def get_success_url(self):
#         return self.object.content.get_absolute_url()


# class CommentDeleteView(LoginRequiredMixin, DeleteView):
#     model = Comment
#     template_name = "comment/delete_comment.html"

#     def get_object(self, queryset=None):
#         comment = super().get_object(queryset)
#         if comment.author != self.request.user:
#             pass
#         return comment

#     def get_success_url(self):
#         return self.object.content.get_absolute_url()


class LikeCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        if user in comment.liked_by.all():
            comment.liked_by.remove(user)
        else:
            comment.like(user.pk)
        return JsonResponse({"success": True, "likes_count": comment.liked_by.count()})


class DislikeCommentView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        comment = get_object_or_404(Comment, pk=self.kwargs.get("pk"))
        if user in comment.disliked_by.all():
            comment.disliked_by.remove(user)
        else:
            comment.dislike(user.pk)
        return JsonResponse(
            {"success": True, "dislikes_count": comment.disliked_by.count()}
        )
