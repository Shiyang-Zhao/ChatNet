from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Story
from .forms import StoryCreateForm, StoryUpdateForm


class StoryListView(ListView):
    model = Story
    context_object_name = "stories"
    template_name = "stories/story_detail.html"
    # paginate_by = 10

    def get_queryset(self):
        return Story.objects.filter(is_archived=False).order_by("-date_posted")


class StoryDetailView(DetailView):
    model = Story
    context_object_name = "story"
    template_name = "stories/story_detail.html"

    def get_queryset(self):
        return Story.objects.filter(is_archived=False)


class StoryCreateView(CreateView):
    model = Story
    form_class = StoryCreateForm
    template_name = "stories/story_create_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("story_detail", kwargs={"pk": self.object.pk})


class StoryUpdateView(UpdateView):
    model = Story
    form_class = StoryUpdateForm
    template_name = "stories/story_update_form.html"

    def get_success_url(self):
        return reverse_lazy("story_detail", kwargs={"pk": self.object.pk})


# class StoryArchiveView(RedirectView):
#     pattern_name = 'story_list'  # Redirect to the story list after archiving

#     def get_redirect_url(self, *args, **kwargs):
#         story = get_object_or_404(Story, pk=kwargs['pk'])
#         story.archive()
#         return super().get_redirect_url(*args, **kwargs)
