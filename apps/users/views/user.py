from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from allauth.account.views import LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from ..forms.user import UserSignUpForm, UserLoginForm
from django.http import HttpResponseRedirect

User = get_user_model()


class UserSignUpView(CreateView):
    form_class = UserSignUpForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect("/?modal=auth")

    def get_success_url(self):
        return "/?modal=auth"


class UserLoginView(LoginView):
    form_class = UserLoginForm
    success_url = reverse_lazy("metasphere")
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me:
            self.request.session.set_expiry(2592000)  # 30 days
        else:
            self.request.session.set_expiry(0)
        return super().form_valid(form)

    def form_invalid(self, form):
        return HttpResponseRedirect("/?modal=auth")


class UserLogoutView(LogoutView):
    pass
