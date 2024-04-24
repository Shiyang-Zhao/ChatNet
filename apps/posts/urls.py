from django.urls import path
from .views.post import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]

# urlpatterns = [
#     path("comments/create/", CommentCreateView.as_view(), name="comment-create"),
#     path(
#         "comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"
#     ),
#     path(
#         "comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
#     ),
# ]
