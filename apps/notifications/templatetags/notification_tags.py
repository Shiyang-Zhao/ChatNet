from django import template
from ..models import Notification

register = template.Library()


@register.simple_tag
def unread_notification_count(user):
    return Notification.objects.filter(receiver=user, is_read=False).count()
