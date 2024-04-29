import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models.chat import Chat
from .models.message import Message
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_pk = self.scope["url_route"]["kwargs"]["pk"]
        self.chat_channel_name = f"chat_{self.chat_pk}"
        self.chat = await sync_to_async(Chat.objects.get)(pk=self.chat_pk)

        await self.channel_layer.group_add(self.chat_channel_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_channel_name, self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.chat_channel_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))

    @database_sync_to_async
    def save_message(self, sender_pk, message):
        User = get_user_model()
        sender = User.objects.get(pk=sender_pk)
        chat = Chat.objects.get(pk=self.chat_pk)
        Message.objects.create(sender=sender, chat=chat, content=message)
