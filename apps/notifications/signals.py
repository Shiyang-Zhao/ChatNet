from django.db.models.signals import post_save
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification
from ..chats.models.message import Message
from asgiref.sync import sync_to_async
from django.template.loader import render_to_string


User = get_user_model()


@receiver(post_save, sender=Message)
def new_message_notification(sender, instance, created, **kwargs):
    if created:
        chat = instance.chat
        receivers = chat.participants.exclude(pk=instance.sender.pk)
        channel_layer = get_channel_layer()
        content = f"You have received a new message from {instance.sender.username} in chat {chat.pk}: {instance.content}"

        for receiver in receivers:
            notification = Notification.objects.create(
                receiver=receiver,
                sender=instance.sender,
                content=content,
            )
            unread_count = Notification.objects.filter(
                receiver=receiver, is_read=False
            ).count()
            payload = {
                "type": "general_notification_message",
                "notification_pk": notification.pk,
                "sender_username": instance.sender.username,
                "content": content,
                "date_sent": notification.date_sent.isoformat(),
                "unread_count": unread_count,
            }

            async def get_chat_html():
                chat_html = await sync_to_async(render_to_string)(
                    "components/chats/chat_item.html",
                    {"user": receiver, "chat": chat},
                )
                return chat_html

            if chat.last_active is None:
                chat_html = async_to_sync(get_chat_html)()
                payload["chat_html"] = chat_html

            async_to_sync(channel_layer.group_send)(
                f"notification_{receiver.pk}", payload
            )
