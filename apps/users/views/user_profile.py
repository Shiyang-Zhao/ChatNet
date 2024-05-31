from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms.user import UserUpdateForm
from ..forms.profile import ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.views.generic.base import View
from apps.stories.models import Story

User = get_user_model()


class UserAndProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_profile_detail.html"
    context_object_name = "viewed_user"

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs.get("username"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_stories"] = Story.active_stories(self.object)
        return context


class UserAndProfileUpdateView(LoginRequiredMixin, View):
    first_form_class = UserUpdateForm
    second_form_class = ProfileUpdateForm
    template_name = "users/user_profile_update_form.html"

    def get(self, request, *args, **kwargs):
        user_update_form = self.first_form_class(instance=request.user)
        profile_update_form = self.second_form_class(instance=request.user.profile)
        return render(
            request,
            self.template_name,
            {
                "user_update_form": user_update_form,
                "profile_update_form": profile_update_form,
            },
        )

    def post(self, request, *args, **kwargs):
        user_update_form = self.first_form_class(request.POST, instance=request.user)
        profile_update_form = self.second_form_class(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_update_form.is_valid() and profile_update_form.is_valid():
            return self.form_valid(request, user_update_form, profile_update_form)
        else:
            return self.form_invalid(request, user_update_form, profile_update_form)

    def form_valid(self, request, user_update_form, profile_update_form):
        user_update_form.save()
        profile_update_form.save()
        messages.success(request, "Your profile has been successfully updated.")
        return redirect(self.get_success_url())

    def form_invalid(self, request, user_update_form, profile_update_form):
        messages.error(
            request,
            "There was a problem with your submission. Please check the details.",
        )
        return render(
            request,
            self.template_name,
            {
                "user_update_form": user_update_form,
                "profile_update_form": profile_update_form,
            },
        )

    def get_success_url(self):
        return reverse_lazy(
            "user-profile-detail", kwargs={"username": self.request.user.username}
        )
