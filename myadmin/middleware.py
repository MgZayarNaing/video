from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.apps import apps
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class UpdateLastActivityMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.user.is_authenticated:
            CustomUser = apps.get_model(settings.AUTH_USER_MODEL)
            CustomUser.objects.filter(id=request.user.id).update(last_activity=timezone.now())
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "user_status", {
                    'type': 'user_status',
                    'message': f'User {request.user.username} is online'
                }
            )
            
        return None
    
    def __call__(self, request):
        response = self.get_response(request)
        
        if request.user.is_authenticated and not request.user.is_active:
            CustomUser = apps.get_model(settings.AUTH_USER_MODEL)
            CustomUser.objects.filter(id=request.user.id).update(last_logout=timezone.now())
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "user_status", {
                    'type': 'user_status',
                    'message': f'User {request.user.username} is offline'
                }
            )
        
        return response
