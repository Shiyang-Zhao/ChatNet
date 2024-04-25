from django.urls import path
from .views.user import UserRegisterView, UserLoginView, UserLogoutView
from .views.user_profile import user_and_profile_detail, user_and_profile_update

urlpatterns = [
    path("signup/", UserRegisterView.as_view(), name="user-register"),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("logout/", UserLogoutView.as_view(), name="user-logout"),
    # path("user/<str:username>/update/", UserUpdateView.as_view(), name="user-update"),
    # path(
    #     "user/<str:username>/profile/detail/",
    #     ProfileDetailView.as_view(),
    #     name="user-profile-detail",
    # ),
    # path(
    #     "user/<str:username>/profile/create/",
    #     ProfileCreateView.as_view(),
    #     name="user-profile-create",
    # ),
    path(
        "user/<str:username>/profile/detail/",
        user_and_profile_detail,
        name="user-profile-detail",
    ),
    path(
        "user/<str:username>/profile/update/",
        user_and_profile_update,
        name="user-profile-update",
    ),
]
