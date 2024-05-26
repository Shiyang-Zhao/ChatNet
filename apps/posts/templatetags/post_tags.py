from django import template

register = template.Library()


@register.simple_tag
def check_post_like_status(post, user):
    if post.liked_by.filter(pk=user.pk).exists():
        return 1
    elif post.disliked_by.filter(pk=user.pk).exists():
        return -1
    else:
        return 0
