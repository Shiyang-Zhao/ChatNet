from django.views.generic import ListView, View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification
from django.http import HttpResponseRedirect
from django.urls import reverse


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = "notifications/notification_detail.html"
    context_object_name = "notifications"

    def get_queryset(self):
        return Notification.objects.filter(receiver=self.request.user).order_by(
            "-date_sent"
        )


class MarkAsReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        Notification.objects.filter(pk=pk, receiver=request.user).update(is_read=True)
        return redirect("notification-list")


class MarkAsUnreadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        Notification.objects.filter(pk=pk, receiver=request.user).update(is_read=False)
        return redirect("notification-list")


class MarkAllAsReadView(LoginRequiredMixin, View):
    def post(self, request):
        Notification.objects.filter(receiver=request.user, is_read=False).update(
            is_read=True
        )
        return redirect("notification-list")
