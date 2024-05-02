from django.urls import path
from .views.post import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    LikePostView,
    DislikePostView,
)

from .views.comment import (
    CommentCreateView,
    ReplyCreateView,
    # CommentUpdateView,
    # CommentDeleteView,
    LikeCommentView,
    DislikeCommentView,
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
        "comment/<int:pk>/reply/",
        ReplyCreateView.as_view(),
        name="reply-create",
    ),
    path("post/<int:pk>/like/", LikePostView.as_view(), name="like-post"),
    path("post/<int:pk>/dislike/", DislikePostView.as_view(), name="dislike-post"),
    path("comment/<int:pk>/like/", LikeCommentView.as_view(), name="like-comment"),
    path(
        "comment/<int:pk>/dislike/",
        DislikeCommentView.as_view(),
        name="dislike-comment",
    ),
]
