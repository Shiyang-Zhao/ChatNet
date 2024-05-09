from django.urls import path
from .views import NotificationListView, MarkAsReadView

urlpatterns = [
    path("", NotificationListView.as_view(), name="notification-list"),
    path("read/<int:pk>/", MarkAsReadView.as_view(), name="mark-as-read"),
]
