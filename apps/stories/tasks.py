from celery import shared_task
from .models import Story


@shared_task
def archive_expired_stories():
    """Task to expire stories that have passed their expiration time."""
    for story in Story.objects.filter(is_archived=False):
        if story.is_expired:
            story.archive()
