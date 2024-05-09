from django.views.generic import ListView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/notification_detail.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).order_by(
            "-created_at"
        )


class MarkAsReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, receiver=request.user)
        notification.is_read = True
        notification.save()
        return redirect("notification-list")
