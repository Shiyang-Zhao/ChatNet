from django.urls import path
from .views.chat import (
    ChatListView,
    PrivateChatForm,
    GroupChatCreateView,
    ChatDetailView,
)

urlpatterns = [
    path("", ChatListView.as_view(), name="chat-list"),
    # path("chat/create/", ChatCreateView.as_view(), name="chat-create"),
    # path("chat/<int:pk>/delete/", ChatDeleteView.as_view(), name="chat-delete"),
    # path("chat/<int:pk>/update/", ChatUpdateView.as_view(), name="chat-update"),
    path("chat/<int:pk>/", ChatDetailView.as_view(), name="chat-detail"),
]
