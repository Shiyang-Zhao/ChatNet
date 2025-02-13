from django.urls import path
from .views import (
    StoryCreateView,
    StoryUpdateView,
    # StorySoftDeleteView,
    StoryDeleteView,
    StoryArchiveView,
)

urlpatterns = [
    # path("", StoryListView.as_view(), name="story-list"),
    # path("story/<int:pk>/", StoryDetailView.as_view(), name="story-detail"),
    path("story/create/", StoryCreateView.as_view(), name="story-create"),
    path("story/<int:pk>/update/", StoryUpdateView.as_view(), name="story-update"),
    path("story/<int:pk>/archive/", StoryArchiveView.as_view(), name="story-archive"),
    path(
        "story/<int:pk>/delete/",
        StoryDeleteView.as_view(),
        name="story-delete",
    ),
]
