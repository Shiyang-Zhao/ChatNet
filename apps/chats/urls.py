from django.urls import path
from .views.chat import (
    ChatListView,
    PrivateChatCreateView,
    GroupChatCreateView,
    ChatDetailView,
)

urlpatterns = [
    path("", ChatListView.as_view(), name="chat-list"),
    path("chat/<int:pk>/", ChatDetailView.as_view(), name="chat-detail"),
    path(
        "chat/private/<str:receiver_username>/create/",
        PrivateChatCreateView.as_view(),
        name="private-chat-create",
    ),
    # path("chat/<int:pk>/delete/", ChatDeleteView.as_view(), name="chat-delete"),
    # path("chat/<int:pk>/update/", ChatUpdateView.as_view(), name="chat-update"),
]
