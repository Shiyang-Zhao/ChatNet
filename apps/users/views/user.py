from django.views.generic import CreateView
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from allauth.account.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from ..forms.user import (
    UserPasswordResetForm,
    UserSetPasswordForm,
    UserSignUpForm,
    UserLoginForm,
)
from django.http import HttpResponseRedirect

User = get_user_model()


class UserSignUpView(CreateView):
    form_class = UserSignUpForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/?modal=signup")

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return HttpResponseRedirect("/?modal=signup")

    def get_success_url(self):
        return "/?modal=login"


class UserLoginView(LoginView):
    form_class = UserLoginForm
    success_url = reverse_lazy("metasphere")
    redirect_authenticated_user = True

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/?modal=login")

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me:
            self.request.session.set_expiry(2592000)  # 30 days
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect("/?modal=login")


class UserLogoutView(LogoutView):
    pass


class UserPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    email_template_name = "apps/users/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")
    template_name = "apps/users/password_reset_form.html"


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = "apps/users/password_reset_done.html"


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    success_url = reverse_lazy("password_reset_complete")
    template_name = "apps/users/password_reset_confirm.html"


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "apps/users/password_reset_complete.html"
