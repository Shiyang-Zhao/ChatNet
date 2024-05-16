from django.urls import path
from .views import StoryListView, StoryDetailView, StoryCreateView

urlpatterns = [
    path("", StoryListView.as_view(), name="story-list"),
    path("story/<int:pk>/", StoryDetailView.as_view(), name="story-detail"),
    path("story/create", StoryCreateView.as_view(), name="story-create"),
    # path('story/archive/<int:pk>/', StoryArchiveView.as_view(), name='story-archive'),
]
