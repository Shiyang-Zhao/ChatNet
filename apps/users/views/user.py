from django.views.generic import FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from ..forms.user import UserRegisterForm

User = get_user_model()


class UserRegisterView(FormView):
    template_name = "users/signup.html"
    form_class = UserRegisterForm

    def get_success_url(self):
        return reverse_lazy("user-login")

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get("username")
        messages.success(self.request, f"Account created for {username}!")
        return super().form_valid(form)


class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")


# class PasswordResetView(PasswordResetView):
