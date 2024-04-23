from django.urls import path
from .views.chat import ChatCreateView, ChatDetailView

urlpatterns = [
    path("chats/create/", ChatCreateView.as_view(), name="chat-create"),
    path("chats/<int:pk>/", ChatDetailView.as_view(), name="chat-detail"),
]
