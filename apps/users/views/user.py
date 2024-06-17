from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from ..forms.user import UserRegisterForm, UserLoginForm

User = get_user_model()


class UserRegisterView(FormView):
    template_name = "apps/users/signup.html"
    form_class = UserRegisterForm

    def get_success_url(self):
        return reverse_lazy("user-login")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        messages.success(self.request, f"Account created for {username}!")
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = "apps/users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("metasphere")

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me:
            self.request.session.set_expiry(2592000)  # 30 days
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("metasphere")


# class PasswordResetView(PasswordResetView):
