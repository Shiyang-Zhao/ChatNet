from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from ..models.chat import Chat
from ..forms.chat import GroupChatCreateForm, PrivateChatCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib import messages

User = get_user_model()


# class ChatListView(LoginRequiredMixin, ListView):
#     model = Chat
#     template_name = "chats/chat_detail.html"
#     # context_object_name = "chats"
#     # ordering = ["-last_activity"]

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["message_form"] = MessageCreateForm()
#         return context


# class ChatDetailView(LoginRequiredMixin, DetailView):
#     model = Chat
#     template_name = "chats/chat_detail.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["message_form"] = MessageCreateForm()
#         return context


class ChatListAndDetailView(View):
    template_name = "chats/chat_detail.html"

    def get(self, request, pk=None):
        context = {
            "chats": Chat.objects.filter(participants=request.user),
            "group_chat_create_form": GroupChatCreateForm(),
        }
        return render(request, self.template_name, context)


class PrivateChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    form_class = PrivateChatCreateForm

    def form_valid(self, form):
        receiver_username = self.kwargs.get("receiver_username")
        receiver = get_object_or_404(User, username=receiver_username)
        existing_chat = Chat.get_existing_private_chat(self.request.user, receiver)

        if existing_chat:
            messages.info(self.request, "Private chat already exists.")
            return redirect(existing_chat.get_absolute_url())

        self.object = form.save(commit=False)
        self.object.creator = self.request.user
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

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.creator = self.request.user
        self.object.chat_type = Chat.GROUP
        self.object.title = "Group Chat"
        self.object.description = "Group Chat"
        self.object.save()
        self.object.participants.add(self.request.user)
        participants = form.cleaned_data.get("participants")
        if participants:
            self.object.participants.add(*participants)
        return super().form_valid(form)
