from django import template

register = template.Library()


@register.simple_tag
def check_comment_like_status(comment, user):
    if comment.liked_by.filter(pk=user.pk).exists():
        return 1
    elif comment.disliked_by.filter(pk=user.pk).exists():
        return -1
    else:
        return 0
