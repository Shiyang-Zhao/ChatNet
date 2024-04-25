from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from ..models.profile import Profile
from ..forms.profile import ProfileForm


class ProfileCreateView(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "users/profile_create_form.html"
    success_url = reverse_lazy("user-profile-detail")

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Profile created successfully.")
        return super().form_valid(form)
