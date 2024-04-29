from django.urls import path
from .views.chat import (
    # ChatListView,
    ChatListAndDetailView,
    PrivateChatCreateView,
    GroupChatCreateView,
    # ChatDetailView,
)
from .views.message import MessageCreateView

urlpatterns = [
    path("", ChatListAndDetailView.as_view(), name="chat-list"),
    path("chat/<int:pk>/", ChatListAndDetailView.as_view(), name="chat-detail"),
    path(
        "chat/private/<str:receiver_username>/create/",
        PrivateChatCreateView.as_view(),
        name="private-chat-create",
    ),
    path(
        "chat/<int:pk>/message/create",
        MessageCreateView.as_view(),
        name="message-create",
    ),
]
