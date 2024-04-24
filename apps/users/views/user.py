from django.views.generic import FormView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ..forms.user import UserRegisterForm
from ..forms.user import UserUpdateForm

User = get_user_model()


class UserRegisterView(FormView):
    template_name = "users/signup.html"  # Template for rendering the form
    form_class = UserRegisterForm  # Form class to use
    success_url = reverse_lazy(
        "user-login"
    )  # Redirect after successful form submission

    def form_valid(self, form):
        form.save()  # Save the user
        username = form.cleaned_data.get("username")
        messages.success(self.request, f"Account created for {username}!")
        return super().form_valid(form)  # Redirect to success_url


class UserLoginView(LoginView):
    template_name = "users/login.html"  # The path to your login template
    success_url = reverse_lazy("home")  # Where to redirect after successful login
    redirect_authenticated_user = True  # Redirect already logged-in users

    def get_success_url(self):
        # Custom logic to define where to redirect after login
        return self.success_url  # Default behavior

    def get_context_data(self, **kwargs):
        # Add any additional context data to the template
        context = super().get_context_data(**kwargs)
        # context["extra_info"] = "Additional context information"
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm  # Form for updating user information
    template_name = ""
    success_url = reverse_lazy("profile_detail")  # Redirect after successful update

    def get_object(self):
        return get_object_or_404(User, username=self.request.user.username)

    def form_valid(self, form):
        messages.success(self.request, "User information updated successfully.")
        return super().form_valid(form)  # Default behavior for form handling
