from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import CreateView, DetailView
from ..models.message import Message
from ..models.chat import Chat
from ..forms.message import MessageCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageCreateForm
    template_name = "chats/chat_detail.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.chat = get_object_or_404(Chat, pk=self.kwargs["pk"])
        return super().form_valid(form)
