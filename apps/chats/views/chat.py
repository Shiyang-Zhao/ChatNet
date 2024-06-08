from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import CreateView
from ..models.chat import Chat
from ..forms.chat import GroupChatCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from PIL import Image
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.template.loader import render_to_string
from metasphere.utils import is_ajax

User = get_user_model()


class ChatListAndDetailView(View):
    template_name = "apps/chats/chat_detail.html"

    def get(self, request, pk=None):
        viewed_chat = None
        if pk:
            viewed_chat = get_object_or_404(Chat, pk=pk, participants=request.user)

        context = {
            "chats": Chat.objects.filter(
                participants=request.user, last_active__isnull=False
            )
            .order_by("-last_active")
            .distinct(),
            "group_chat_create_form": GroupChatCreateForm(creator=request.user),
            "selected": viewed_chat is not None,
        }

        if is_ajax(request) and viewed_chat:
            message_html = render_to_string(
                "components/chats/message_item.html",
                {"chat": viewed_chat},
                request=request,
            )
            return JsonResponse({"message_html": message_html}, status=200)

        return render(request, self.template_name, context)


class PrivateChatCreateView(LoginRequiredMixin, CreateView):
    model = Chat
    fields = []

    def form_valid(self, form):
        receiver_username = self.kwargs.get("receiver_username")
        receiver = get_object_or_404(User, username=receiver_username)
        existing_chat = Chat.get_existing_private_chat(self.request.user, receiver)

        if existing_chat:
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


# class PrivateChatCreateView(LoginRequiredMixin, CreateView):
#     model = Chat
#     fields = []

#     def form_valid(self, form):
#         receiver_username = self.kwargs.get("receiver_username")
#         receiver = get_object_or_404(User, username=receiver_username)
#         existing_chat = Chat.get_existing_private_chat(self.request.user, receiver)

#         if existing_chat:
#             if is_ajax(self.request):
#                 return JsonResponse(
#                     {"status": "exists", "url": existing_chat.get_absolute_url()},
#                     status=200,
#                 )
#             else:
#                 return redirect(existing_chat.get_absolute_url())

#         self.object = form.save(commit=False)
#         self.object.save()
#         self.object.participants.add(self.request.user, receiver)

#         if is_ajax(self.request):
#             message_html = render_to_string(
#                 "apps/chats/message_detail.html", {"chat": self.object}, request=self.request
#             )
#             return JsonResponse({"status": "created", "url": self.object.get_absolute_url(), "html": message_html}, status=200)

#         return super().form_valid(form)


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
