from django.shortcuts import render
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Story
from .forms import StoryCreateForm, StoryUpdateForm


# class StoryListView(ListView):
#     model = Story
#     context_object_name = "stories"
#     template_name = "stories/story_detail.html"
#     paginate_by = 10

#     def get_queryset(self):
#         return Story.objects.filter(is_archived=False).order_by("-date_posted")


# class StoryDetailView(DetailView):
#     model = Story
#     context_object_name = "story"
#     template_name = "stories/story_detail.html"

#     def get_queryset(self):
#         return Story.objects.filter(is_archived=False)


class StoryCreateView(LoginRequiredMixin, CreateView):
    model = Story
    form_class = StoryCreateForm
    template_name = "stories/story_create_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # return reverse_lazy("story-list", kwargs={"pk": self.object.pk})
        return reverse_lazy(
            "user-profile-detail", kwargs={"username": self.request.user.username}
        )


class StoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Story
    form_class = StoryUpdateForm
    template_name = "stories/story_update_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "user-profile-detail", kwargs={"username": self.request.user.username}
        )

    def test_func(self):
        story = self.get_object()
        return self.request.user == story.author


class StoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Story

    def get_success_url(self):
        return reverse_lazy(
            "user-profile-detail", kwargs={"username": self.request.user.username}
        )

    def test_func(self):
        story = self.get_object()
        return self.request.user == story.author


# class StoryArchiveView(RedirectView):
#     pattern_name = 'story_list'  # Redirect to the story list after archiving

#     def get_redirect_url(self, *args, **kwargs):
#         story = get_object_or_404(Story, pk=kwargs['pk'])
#         story.archive()
#         return super().get_redirect_url(*args, **kwargs)
