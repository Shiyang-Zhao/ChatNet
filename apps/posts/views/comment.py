from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from ..models.comment import Comment
from ..forms.comment import CommentForm


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment/create_comment.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.content.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comment/edit_comment.html"

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if comment.author != self.request.user:
            # Handle unauthorized access here
            pass
        return comment

    def get_success_url(self):
        return self.object.content.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "comment/delete_comment.html"

    def get_object(self, queryset=None):
        comment = super().get_object(queryset)
        if comment.author != self.request.user:
            # Handle unauthorized access here
            pass
        return comment

    def get_success_url(self):
        return self.object.content.get_absolute_url()
