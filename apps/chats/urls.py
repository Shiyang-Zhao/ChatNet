from django.urls import path
from .views.chat import (
    ChatListAndDetailView,
    PrivateChatCreateView,
    GroupChatCreateView,
)

urlpatterns = [
    path("", ChatListAndDetailView.as_view(), name="chat-list"),
    path("chat/<int:pk>/", ChatListAndDetailView.as_view(), name="chat-detail"),
    path(
        "chat/private/<str:receiver_username>/create/",
        PrivateChatCreateView.as_view(),
        name="private-chat-create",
    ),
    path(
        "chat/group/<str:creator_username>/create/",
        GroupChatCreateView.as_view(),
        name="group-chat-create",
    ),
]
