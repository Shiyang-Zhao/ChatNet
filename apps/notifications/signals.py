from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification
from ..chats.models.message import Message


User = get_user_model()


@receiver(post_save, sender=Message)
def new_message_notification(sender, instance, created, **kwargs):
    if created:
        chat = instance.chat
        sender = instance.sender

        receivers = chat.participants.exclude(pk=sender.pk)
        for receiver in receivers:
            Notification.objects.create(
                user=receiver,
                title="New Message",
                content=f"You have received a new message from {sender.username} in chat '{chat.pk}'.",
                message=instance,
            )
