# yourappname/middleware.py

from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.last_activity = timezone.now()
            request.user.save(update_fields=['last_activity'])

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "user_status", {
                    'type': 'user_status',
                    'message': f'User {request.user.username} is online'
                }
            )

        response = self.get_response(request)

        # Send notification on user registration
        if request.path == '/users/register/' and request.method == 'POST':
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications", {
                    'type': 'send_notification',
                    'message': 'A new user has registered.'
                }
            )

        if request.user.is_authenticated and not request.user.is_active:
            request.user.last_logout = timezone.now()
            request.user.save(update_fields=['last_logout'])

        return response
