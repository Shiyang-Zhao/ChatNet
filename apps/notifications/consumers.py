import json
from channels.generic.websocket import AsyncWebsocketConsumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.notification_channel_name = f"notification_{self.user.pk}"

        await self.channel_layer.group_add(
            self.notification_channel_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.notification_channel_name, self.channel_name
        )

    async def notification_message(self, event):
        content = event["content"]

        await self.send(
            text_data=json.dumps(
                {
                    "type": "notification_message",
                    "content": content,
                }
            )
        )
