import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models.chat import Chat
from apps.users.models.user import User
from .models.message import Message
from django.utils import timezone
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope["query_string"]
        query_params = parse_qs(query_string)
        self.session_id = query_params.get("sid", [None])[0]
        self.connection_id = query_params.get("cid", [None])[0]
        self.chat_channel_name = None

        await self.accept()

    async def disconnect(self, close_code):
        if self.chat_channel_name:
            await self.channel_layer.group_discard(
                self.chat_channel_name, self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")
        chat_pk = text_data_json.get("chat_pk")
        sender = self.scope["user"]

        if message_type == "chat_message":
            new_chat_channel_name = f"chat_{chat_pk}"
            if self.chat_channel_name != new_chat_channel_name:
                if self.chat_channel_name:
                    await self.channel_layer.group_discard(
                        self.chat_channel_name, self.channel_name
                    )
                self.chat_channel_name = new_chat_channel_name
                await self.channel_layer.group_add(
                    self.chat_channel_name, self.channel_name
                )
            content = text_data_json.get("content", "")
            
            try:
                chat = await self.get_chat(chat_pk)
            except ObjectDoesNotExist:
                return

            message = await self.save_message(chat, sender, content, timezone.now())
            message_html = await sync_to_async(render_to_string)(
                "components/chats/message_item.html",
                {"message": message},
            )
            payload = {
                "type": "chat_message",
                "sender_pk": sender.pk,
                "chat_pk": chat_pk,
                "message_html": message_html,
                "sid": self.session_id,
                "cid": self.connection_id,
            }

            if chat.last_active is None:
                chat_html = await sync_to_async(render_to_string)(
                    "components/chats/chat_item.html",
                    {"user": sender, "chat": chat},
                )
                payload["chat_html"] = chat_html

            await self.channel_layer.group_send(self.chat_channel_name, payload)

            chat.last_active = timezone.now()
            await self.update_chat_last_active(chat_pk)
            await self.update_user_last_active(sender.pk)

    async def chat_message(self, event):
        sender_pk = event["sender_pk"]
        chat_pk = event["chat_pk"]
        message_html = event["message_html"]
        session_id = event["sid"]
        connection_id = event["cid"]

        payload = {
            "type": "chat_message",
            "sender_pk": sender_pk,
            "chat_pk": chat_pk,
            "message_html": message_html,
            "sid": session_id,
            "cid": connection_id,
        }

        if "chat_html" in event:
            payload["chat_html"] = event["chat_html"]

        await self.send(text_data=json.dumps(payload))

    @database_sync_to_async
    def save_message(self, chat, sender, content, date_sent):
        return Message.objects.create(
            chat=chat,
            sender=sender,
            content=content,
            date_sent=date_sent,
        )

    @database_sync_to_async
    def update_user_last_active(self, user_pk):
        User.objects.filter(pk=user_pk).update(last_active=timezone.now())

    @database_sync_to_async
    def update_chat_last_active(self, chat_pk):
        Chat.objects.filter(pk=chat_pk).update(last_active=timezone.now())

    @database_sync_to_async
    def get_chat(self, pk):
        return Chat.objects.get(pk=pk)

    @database_sync_to_async
    def get_profile_image_url(self, user):
        return user.profile.profile_image.url
