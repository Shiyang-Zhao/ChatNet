# apps/users/adapter.py

from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.models import SocialAccount
from allauth.account.utils import perform_login
from allauth.socialaccount.providers.github.provider import GitHubProvider
from django.contrib.auth import get_user_model
import requests
import random
import string

User = get_user_model()


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        user = sociallogin.user
        if not user.email:
            if sociallogin.account.provider == GitHubProvider.id:
                user.email = self.get_email_from_github(sociallogin)

        try:
            existing_user = User.objects.get(email=user.email)
            sociallogin.connect(request, existing_user)
            # Automatically log in the user
            perform_login(request, existing_user, email_verification="optional")
        except User.DoesNotExist:
            base_username = user.username or user.email.split("@")[0]
            user.username = self.generate_unique_username(base_username)
            user.save()
            sociallogin.connect(request, user)
            # Automatically log in the user
            perform_login(request, user, email_verification="optional")

    def get_email_from_github(self, sociallogin):
        token = sociallogin.token.token
        headers = {"Authorization": f"token {token}"}
        response = requests.get("https://api.github.com/user/emails", headers=headers)
        emails = response.json()
        primary_emails = [
            email for email in emails if email.get("primary") and email.get("verified")
        ]
        print(emails)

        if primary_emails:
            return primary_emails[0].get("email")
        elif emails:
            return emails[0].get("email")
        else:
            random_suffix = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=8)
            )
            return f"user_{random_suffix}@example.com"

    def generate_unique_username(self, base_username, length=4):
        username = base_username
        while User.objects.filter(username=username).exists():
            random_suffix = "".join(
                random.choices(string.ascii_letters + string.digits, k=length)
            )
            username = f"{base_username}{random_suffix}"
        return username
