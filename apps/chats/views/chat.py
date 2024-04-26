from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from ..models.chat import Chat
from ..forms.chat import PrivateChatForm, GroupChatForm


class ChatListView(ListView):
    model = Chat
    template_name = "chats/chat_detail.html"
    context_object_name = "chats"
    ordering = ["-created_at"]

    def get_queryset(self):
        return Chat.objects.filter(participants=self.request.user)


class ChatDetailView(DetailView):
    model = Chat
    template_name = "chats/chat_detail.html"


class PrivateChatCreateView(CreateView):
    model = Chat
    form_class = PrivateChatForm
    template_name = "chats/create_chat.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class GroupChatCreateView(CreateView):
    model = Chat
    form_class = GroupChatForm
    template_name = "chats/create_chat.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
