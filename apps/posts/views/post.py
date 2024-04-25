from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from ..models.post import Post
from ..forms.post import PostForm
from ..forms.comment import CommentForm, ReplyForm


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
        context["comment_create_form"] = CommentForm()
        context["reply_create_form"] = ReplyForm()
        context["parent_comments"] = post.comments.filter(parent_comment__isnull=True)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_create_form.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully.")
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "posts/post_update_form.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs["pk"], author=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully.")
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "posts/post_confirm_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs["pk"], author=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully.")
        return super().delete(request, *args, **kwargs)
