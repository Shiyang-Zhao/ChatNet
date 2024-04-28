from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView
from ..models.chat import Chat
from ..forms.chat import GroupChatCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

User = get_user_model()


class ChatListView(LoginRequiredMixin, ListView):
    model = Chat
    template_name = "chats/chat_list.html"
    ordering = ["-created_at"]


class ChatDetailView(LoginRequiredMixin, DetailView):
    model = Chat
    template_name = "chats/chat_list.html"


class PrivateChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    fields = []

    def form_valid(self, form):
        receiver_username = self.kwargs.get("receiver_username")
        receiver = get_object_or_404(User, username=receiver_username)
        self.object = form.save(commit=False)
        self.object.chat_type = Chat.PRIVATE
        self.object.creator = self.request.user
        self.object.title = receiver.username
        self.object.save()
        self.object.participants.add(self.request.user, receiver)
        return super().form_valid(form)


class GroupChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    form_class = GroupChatCreateForm
    template_name = "chats/create_chat.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
