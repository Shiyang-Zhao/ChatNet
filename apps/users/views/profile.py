from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from ..models.profile import Profile
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.views import View


class FollowProfileView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_profile = request.user.profile
        target_profile = get_object_or_404(Profile, user__username=username)

        user_profile.follow(target_profile)
        return redirect("user-profile-detail", username=username)


class UnfollowProfileView(LoginRequiredMixin, View):
    def post(self, request, username):
        user_profile = request.user.profile
        target_profile = get_object_or_404(Profile, user__username=username)

        user_profile.unfollow(target_profile)
        return redirect("user-profile-detail", username=username)
