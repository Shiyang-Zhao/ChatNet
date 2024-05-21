from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from ..models.chat import Chat
from ..forms.chat import GroupChatCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse

User = get_user_model()


class ChatListAndDetailView(View):
    template_name = "chats/chat_detail.html"

    def get(self, request, pk=None):
        context = {
            "chats": Chat.objects.filter(Q(participants=request.user)).distinct(),
            "group_chat_create_form": GroupChatCreateForm(creator=request.user),
        }
        return render(request, self.template_name, context)


class PrivateChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    fields = []

    def form_valid(self, form):
        receiver_username = self.kwargs.get("receiver_username")
        receiver = get_object_or_404(User, username=receiver_username)
        existing_chat = Chat.get_existing_private_chat(self.request.user, receiver)

        if existing_chat:
            messages.info(self.request, "Private chat already exists.")
            return redirect(existing_chat.get_absolute_url())

        self.object = form.save(commit=False)
        # self.object.creator = self.request.user
        self.object.title = (
            f"Chat between {self.request.user.username} and {receiver.username}"
        )
        self.object.description = f"Private conversation initiated between {self.request.user.username} and {receiver.username}"
        self.object.save()
        self.object.participants.add(self.request.user, receiver)
        return super().form_valid(form)


class GroupChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    form_class = GroupChatCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["creator"] = self.request.user
        return kwargs

    def form_valid(self, form):
        creator = self.request.user
        participants = form.cleaned_data.get("participants")
        existing_chat = Chat.get_existing_group_chat(participants, creator)
        if existing_chat:
            return redirect(existing_chat.get_absolute_url())

        form.instance.creator = self.request.user
        form.instance.chat_type = Chat.GROUP
        form.instance.title = "Group Title"
        form.instance.description = "Group Description"
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect(f"{reverse('chat-list')}?group_chat_create_form=open")
