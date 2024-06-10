import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Notification
from channels.db import database_sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.notification_channel_name = f"notification_{self.user.pk}"

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.notification_channel_name, self.channel_name
            )
            await self.accept()
            await self.initial_notification_message()
        else:
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.notification_channel_name, self.channel_name
        )

    async def initial_notification_message(self):
        if not self.user.is_authenticated:
            return

        unread_count = await self.get_unread_notification_count()
        await self.send(
            text_data=json.dumps(
                {
                    "type": "initial_notification_message",
                    "unread_count": unread_count,
                }
            )
        )

    async def general_notification_message(self, event):
        if not self.user.is_authenticated:
            return
        notification_pk = event["notification_pk"]
        content = event["content"]
        date_sent = event["date_sent"]
        sender_username = event["sender_username"]
        unread_count = await self.get_unread_notification_count()
        chat_html = event.get("chat_html", None)
        payload = {
            "type": "general_notification_message",
            "notification_pk": notification_pk,
            "sender_username": sender_username,
            "content": content,
            "date_sent": date_sent,
            "unread_count": unread_count,
        }
        if chat_html:
            payload["chat_html"] = chat_html

        await self.send(text_data=json.dumps(payload))

    async def get_unread_notification_count(self):
        @database_sync_to_async
        def get_count():
            return Notification.objects.filter(
                receiver=self.user, is_read=False
            ).count()

        return await get_count()
