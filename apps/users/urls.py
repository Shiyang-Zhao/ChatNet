from django.urls import path
from .views.user import UserRegisterView, UserLoginView, UserUpdateView, UserLogoutView
from .views.profile import ProfileCreateView, ProfileUpdateView, ProfileDetailView

urlpatterns = [
    path("signup/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
    path("user/<str:username>/update/", UserUpdateView.as_view(), name="user-update"),
    path(
        "user/<str:username>/profile/detail/",
        ProfileDetailView.as_view(),
        name="profile-detail",
    ),
    path(
        "user/<str:username>/profile/create/",
        ProfileCreateView.as_view(),
        name="profile-create",
    ),
    path(
        "user/<str:username>/profile/update/",
        ProfileUpdateView.as_view(),
        name="profile-update",
    ),
]
