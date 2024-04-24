from django.urls import path
from django.contrib.auth.views import LoginView
from .views.user import UserRegisterView, UserLoginView, UserUpdateView
from .views.profile import ProfileCreateView, ProfileUpdateView, ProfileDetailView

urlpatterns = [
    path("signup/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("user/update/", UserUpdateView.as_view(), name="user-update"),
    path("user/profile/detail/", ProfileDetailView.as_view(), name="profile-detail"),
    path("user/profile/create/", ProfileCreateView.as_view(), name="profile-create"),
    path("user/profile/update/", ProfileUpdateView.as_view(), name="profile-update"),
]
