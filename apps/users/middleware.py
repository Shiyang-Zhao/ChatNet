from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.sites.models import Site

User = get_user_model()


class UpdateUserLastActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            User.objects.filter(pk=request.user.pk).update(last_active=timezone.now())
        return response


class UpdateSiteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        site = Site.objects.get(id=1)
        site.name = "Metasphere"
        site.domain = "127.0.0.1:8000"
        site.save()

        response = self.get_response(request)
        return response
