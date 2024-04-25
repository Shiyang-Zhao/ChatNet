from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from ..models.chat import Chat
from ..forms.chat import ChatCreationForm


class ChatListView(ListView):
    model = Chat
    template_name = "chats/chat_detail.html"
    context_object_name = "chats"
    ordering = ["-created_at"]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)


class ChatDetailView(DetailView):
    model = Chat
    template_name = "chat/chat_detail.html"


class ChatCreateView(CreateView):
    model = Chat
    form_class = ChatCreationForm
    template_name = "chat/create_chat.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
