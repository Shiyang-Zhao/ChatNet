from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from ..models.comment import Comment
from ..models.post import Post
from ..forms.comment import CommentForm, ReplyForm


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "posts/post_detail.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs.get("pk"))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})


class ReplyCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = ReplyForm
    template_name = "posts/post_detail.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        parent_comment = get_object_or_404(Comment, pk=self.kwargs.get("parent_comment_pk"))
        form.instance.parent_comment = parent_comment
        form.instance.post = parent_comment.post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.post.pk})


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
