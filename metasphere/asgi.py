"""
ASGI config for Metasphere project.

It exposes the ASGI callable as a module-level variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Step 1: Set the environment variable for Django's settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metasphere.settings")

# Step 2: Initialize Django ASGI application early to setup Django
django_asgi_app = get_asgi_application()

# Step 3: Now import any Django-dependent modules
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from apps.chats.routing import websocket_urlpatterns as chat_patterns
from apps.notifications.routing import websocket_urlpatterns as notification_patterns

# Now setup the application protocol router
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,  # Mount the ASGI application to handle HTTP requests
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter([*chat_patterns, *notification_patterns]))
        ),
    }
)
