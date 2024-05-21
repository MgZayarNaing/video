# yourappname/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/status/', consumers.UserStatusConsumer.as_asgi()),
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]
