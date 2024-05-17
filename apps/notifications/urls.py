from django.urls import path
from .views import (
    NotificationListView,
    MarkAsReadView,
    MarkAsUnreadView,
    MarkAllAsReadView,
)

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("notification/<int:pk>/read/", MarkAsReadView.as_view(), name="mark-as-read"),
    path(
        "notification/<int:pk>/unread/",
        MarkAsUnreadView.as_view(),
        name="mark-as-unread",
    ),
    path("notification/read/all/", MarkAllAsReadView.as_view(), name="mark-all-as-read"),
]
