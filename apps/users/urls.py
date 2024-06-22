from django.urls import path, include
from .views.user import UserRegisterView, UserLoginView, UserLogoutView
from .views.profile import FollowProfileView, UnfollowProfileView
from .views.user_profile import UserAndProfileDetailView, UserAndProfileUpdateView

urlpatterns = [
    path("signup/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
    path(
        "user/<str:username>/profile/detail/",
        UserAndProfileDetailView.as_view(),
        name="user-profile-detail",
    ),
    path(
        "user/profile/update/",
        UserAndProfileUpdateView.as_view(),
        name="user-profile-update",
    ),
    path(
        "user/<str:username>/profile/follow/",
        FollowProfileView.as_view(),
        name="follow-profile",
    ),
    path(
        "user/<str:username>/profile/unfollow/",
        UnfollowProfileView.as_view(),
        name="unfollow-profile",
    ),
]
