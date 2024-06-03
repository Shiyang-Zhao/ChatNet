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
from PIL import Image
from pathlib import Path
from django.conf import settings
import os

User = get_user_model()


class ChatListAndDetailView(View):
    template_name = "apps/chats/chat_detail.html"

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

        chat = form.save(commit=False)
        chat.creator = creator
        chat.chat_type = Chat.GROUP

        participant_usernames = [user.username for user in participants]
        chat.title = self.generate_chat_title(participant_usernames)
        chat.description = self.generate_chat_description(
            creator, participants, chat.title
        )
        chat.save()

        profile_images = [user.profile.profile_image.path for user in participants[:9]]
        chat.image = self.create_chat_image(profile_images, chat.pk)
        chat.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        return redirect(f"{reverse('chat-list')}?group_chat_create_form=open")

    def generate_chat_title(self, participant_usernames):
        if len(participant_usernames) > 2:
            return f"{participant_usernames[0]}, {participant_usernames[1]}, and more"
        return ", ".join(participant_usernames)

    def generate_chat_description(self, creator, participants, title):
        participant_count = len(participants)
        if participant_count > 2:
            return f"A group chat created by {creator.username} with {participant_count} participants."
        return f"A group chat created by {creator.username} with {title}."

    def create_chat_image(self, profile_images, chat_pk):
        images = [Image.open(image_path) for image_path in profile_images]
        num_images = len(images)
        size = 100
        new_image = Image.new(
            "RGB",
            (min(num_images, 3) * size, ((num_images + 2) // 3) * size),
            (255, 255, 255),
        )
        for index, image in enumerate(images):
            row = index // 3
            col = index % 3
            image = image.resize((size, size), Image.Resampling.LANCZOS)
            new_image.paste(image, (col * size, row * size))

        chat_image_dir = Path(settings.MEDIA_ROOT) / "chat_images" / f"chat_{chat_pk}"
        chat_image_dir.mkdir(parents=True, exist_ok=True)
        chat_image_name = f"chat_image_{chat_pk}.jpg"
        chat_image_path = chat_image_dir / chat_image_name
        new_image.save(chat_image_path)

        return str(chat_image_path.relative_to(settings.MEDIA_ROOT))
