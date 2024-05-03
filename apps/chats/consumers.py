import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models.chat import Chat
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
        message_content = text_data_json.get("content", "")
        sender = self.scope["user"]
        date_sent = timezone.now()

        # Save the message to the database
        await self.save_message(sender, message_content, date_sent)

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.chat_channel_name,
            {
                "type": "chat_message",
                "sender_username": sender.username,
                "content": message_content,
                "date_sent": date_sent.isoformat(),
            },
        )

    # Consumer sends message
    async def chat_message(self, event):
        sender_username = event["sender_username"]
        content = event["content"]
        date_sent = event["date_sent"]

        # Send the message to the client
        await self.send(
            text_data=json.dumps(
                {
                    "sender_username": sender_username,
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
    def get_chat(self, pk):
        return Chat.objects.get(pk=pk)
