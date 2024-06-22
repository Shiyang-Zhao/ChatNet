from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth import get_user_model
import random
import string

User = get_user_model()


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        try:
            existing_user = User.objects.get(email=user.email)
            sociallogin.connect(request, existing_user)
        except User.DoesNotExist:
            base_username = user.username or user.email.split("@")[0]
            user.username = self.generate_unique_username(base_username)
            user.save()

    def generate_unique_username(self, base_username, length=4):
        username = base_username
        while User.objects.filter(username=username).exists():
            random_suffix = "".join(
                random.choices(string.ascii_letters + string.digits, k=length)
            )
            username = f"{base_username}{random_suffix}"
        return username
