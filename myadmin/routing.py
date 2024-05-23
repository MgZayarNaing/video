# yourappname/routing.py

from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/user_status/', consumers.StatusConsumer.as_asgi()),
]
