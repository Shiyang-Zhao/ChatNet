from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404
from ..models.profile import Profile
from ..forms.profile import ProfileForm


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "users/profile_detail.html"  # Template to display profile details

    def get_object(self):
        # Retrieve the current user's profile
        return get_object_or_404(Profile, user=self.request.user)


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "users/profile_create_form.html"
    success_url = reverse_lazy("profile_detail")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Profile created successfully.")
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "users/profile_update_form.html"
    success_url = reverse_lazy("profile_detail")

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)
