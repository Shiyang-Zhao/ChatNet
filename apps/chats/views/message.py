from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView
from ..models.message import Message
from ..forms.message import MessageCreationForm


class MessageDetailView(DetailView):
    model = Message
    template_name = "chat/message_detail.html"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageCreationForm
    template_name = "chat/create_message.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
