from django.urls import path
from .views.chat import ChatCreateView, ChatDetailView

urlpatterns = [
    path("chat/create/", ChatCreateView.as_view(), name="chat-create"),
    path("chat/<int:pk>/", ChatDetailView.as_view(), name="chat-detail"),
]
