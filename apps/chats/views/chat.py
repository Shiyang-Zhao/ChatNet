from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, CreateView, DetailView
from ..models.chat import Chat
from ..forms.chat import GroupChatCreateForm, PrivateChatCreateForm
from ..forms.message import MessageCreateForm
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
            "message_form": MessageCreateForm(),
        }
        return render(request, self.template_name, context)


class PrivateChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    form_class = PrivateChatCreateForm

    def form_valid(self, form):
        receiver_username = self.kwargs.get("receiver_username")
        receiver = get_object_or_404(User, username=receiver_username)
        # Check for an existing private chat between the request user and the receiver
        existing_chat = Chat.get_existing_private_chat(self.request.user, receiver)

        if existing_chat:
            messages.info(self.request, "Private chat already exists.")
            return redirect(existing_chat.get_absolute_url())

        self.object = form.save(commit=False)
        self.object.creator = self.request.user
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
