from django.urls import path
from .views.post import (
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostHardDeleteView,
    PostSoftDeleteView,
    LikePostView,
    DislikePostView,
    SavePostView,
    UnsavePostView,
)

from .views.comment import (
    CommentDetailView,
    CommentCreateView,
    ReplyCreateView,
    CommentUpdateView,
    CommentSoftDeleteView,
    CommentHardDeleteView,
    LikeCommentView,
    DislikeCommentView,
    SaveCommentView,
    UnsaveCommentView,
)

urlpatterns = [
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path(
        "post/<int:pk>/soft/delete/",
        PostSoftDeleteView.as_view(),
        name="post-soft-delete",
    ),
    path(
        "post/<int:pk>/hard/delete/",
        PostHardDeleteView.as_view(),
        name="post-hard-delete",
    ),
    path("post/<int:pk>/like/", LikePostView.as_view(), name="like-post"),
    path("post/<int:pk>/dislike/", DislikePostView.as_view(), name="dislike-post"),
    path("post/<int:pk>/save/", SavePostView.as_view(), name="save-post"),
    path("post/<int:pk>/unsave/", UnsavePostView.as_view(), name="unsave-post"),
    path(
        "post/<int:post_pk>/comment/<int:pk>/",
        CommentDetailView.as_view(),
        name="comment-detail",
    ),
    path(
        "post/<int:pk>/comment/create/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comment/<int:pk>/reply/",
        ReplyCreateView.as_view(),
        name="reply-create",
    ),
    path(
        "comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-update"
    ),
    path(
        "comment/<int:pk>/soft/delete/",
        CommentSoftDeleteView.as_view(),
        name="comment-soft-delete",
    ),
    path(
        "comment/<int:pk>/hard/delete/",
        CommentHardDeleteView.as_view(),
        name="comment-hard-delete",
    ),
    path("comment/<int:pk>/like/", LikeCommentView.as_view(), name="like-comment"),
    path(
        "comment/<int:pk>/dislike/",
        DislikeCommentView.as_view(),
        name="dislike-comment",
    ),
    path("comment/<int:pk>/save/", SaveCommentView.as_view(), name="save-comment"),
    path(
        "comment/<int:pk>/unsave/", UnsaveCommentView.as_view(), name="unsave-comment"
    ),
]
