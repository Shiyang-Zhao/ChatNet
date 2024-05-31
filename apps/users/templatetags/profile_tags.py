from django import template

register = template.Library()


@register.simple_tag
def check_profile_follow_status(user, viewed_user):
    return user.profile.is_following(viewed_user.profile)
