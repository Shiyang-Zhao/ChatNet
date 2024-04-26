from django.urls import path
from .views.user import UserRegisterView, UserLoginView, UserLogoutView
from .views.profile import FollowProfileView, UnfollowProfileView
from .views.user_profile import user_and_profile_detail, user_and_profile_update

urlpatterns = [
    path("signup/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
    path(
        "user/<str:username>/profile/detail/",
        user_and_profile_detail,
        name="user-profile-detail",
    ),
    path(
        "user/profile/update/",
        user_and_profile_update,
        name="user-profile-update",
    ),
    path(
        "user/<str:username>/profile/follow",
        FollowProfileView.as_view(),
        name="follow-profile",
    ),
    path(
        "user/<str:username>/profile/unfollow",
        UnfollowProfileView.as_view(),
        name="unfollow-profile",
    ),
]
