from django.urls import path
from .consumers import ChatConsumer

# websocket_urlpatterns = [
#     path("ws/chats/chat/<int:pk>/", ChatConsumer.as_asgi()),
# ]

websocket_urlpatterns = [
    path("ws/chats/", ChatConsumer.as_asgi()),
]
