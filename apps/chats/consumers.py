import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models.chat import Chat
from apps.users.models.user import User
from .models.message import Message
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.chat = await self.get_chat(self.chat_pk)
        self.chat_channel_name = f"chat_{self.chat_pk}"

        await self.channel_layer.group_add(self.chat_channel_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_channel_name, self.channel_name
        )

    # Consumer receives message
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")
        sender = self.scope["user"]

        if message_type == "chat_message":
            content = text_data_json.get("content", "")
            date_sent = timezone.now()

            # Save message to the database
            await self.save_message(sender, content, date_sent)
            await self.update_user_last_active(sender.pk)
            await self.update_chat_last_active(self.chat_pk)
            sender_profile_image_url = await self.get_profile_image_url(sender)
            # Send the chat message to the chat group
            await self.channel_layer.group_send(
                self.chat_channel_name,
                {
                    "type": "chat_message",
                    "sender_username": sender.username,
                    "sender_profile_image_url": sender_profile_image_url,
                    "content": content,
                    "date_sent": date_sent.isoformat(),
                },
            )

    async def chat_message(self, event):
        sender_username = event["sender_username"]
        sender_profile_image_url = event["sender_profile_image_url"]
        content = event["content"]
        date_sent = event["date_sent"]

        # Send the message to the client
        await self.send(
            text_data=json.dumps(
                {
                    "type": "chat_message",
                    "sender_username": sender_username,
                    "sender_profile_image_url": sender_profile_image_url,
                    "content": content,
                    "date_sent": date_sent,
                }
            )
        )

    @database_sync_to_async
    def save_message(self, sender, content, date_sent):
        return Message.objects.create(
            chat=self.chat,
            sender=sender,
            content=content,
            date_sent=date_sent,
        )

    @database_sync_to_async
    def update_user_last_active(self, user_pk):
        """Update the user's last active timestamp."""
        User.objects.filter(pk=user_pk).update(last_active=timezone.now())

    @database_sync_to_async
    def update_chat_last_active(self, chat_pk):
        """Update the chat's last active timestamp."""
        Chat.objects.filter(pk=chat_pk).update(last_active=timezone.now())

    @database_sync_to_async
    def get_chat(self, pk):
        return Chat.objects.get(pk=pk)

    @database_sync_to_async
    def get_profile_image_url(self, user):
        return user.profile.profile_image.url
