from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..forms.user import UserUpdateForm
from ..forms.profile import ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView

User = get_user_model()


class UserAndProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/user_profile_detail.html"
    context_object_name = "viewed_user"

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs["username"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_following"] = self.request.user.profile.is_following(
            self.object.profile
        )
        return context


@login_required
def user_and_profile_update(request):
    user = request.user
    if request.method == "POST":
        user_update_form = UserUpdateForm(request.POST, instance=user)
        profile_update_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=user.profile
        )

        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()

            messages.success(request, "Your profile has been updated successfully!")
            return redirect("user-profile-detail", username=user.username)
        else:
            messages.error(
                request,
                "Fail to update your profile.",
            )
    else:
        user_update_form = UserUpdateForm(instance=user)
        profile_update_form = ProfileUpdateForm(instance=user.profile)

    context = {
        "user_update_form": user_update_form,
        "profile_update_form": profile_update_form,
    }

    return render(request, "users/user_profile_update_form.html", context)
