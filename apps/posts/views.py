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
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    model = Post  # The model to fetch from the database
    template_name = "posts/post_list.html"  # Template to render the list
    context_object_name = "posts"  # Context variable for the list of posts
    paginate_by = 10  # Number of items per page
    ordering = ["-date_posted"]


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"

    def get_object(self):
        return get_object_or_404(Post, pk=self.kwargs["pk"])


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
