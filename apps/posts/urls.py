from django.urls import path
from .views.post import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
)

from .views.comment import (
    CommentCreateView,
    ReplyCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path(
        "post/<int:pk>/comment/create",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "post/<int:post_pk>/comment/<int:parent_comment_pk>/reply/",
        ReplyCreateView.as_view(),
        name="reply-create",
    ),
]

# urlpatterns = [
#
#     path(
#         "comments/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"
#     ),
#     path(
#         "comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
#     ),
# ]
