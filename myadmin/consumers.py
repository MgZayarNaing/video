from channels.generic.websocket import AsyncWebsocketConsumer
import json

class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        # User logged out, update status to offline
        await self.update_user_status(self.scope['user'], 'offline')

    async def update_user_status(self, user, status):
        # Logic to update user's status in the database
        # Broadcast status update to all connected clients
        await self.channel_layer.group_send(
            'status_group',
            {
                'type': 'user.status',
                'message': {'user': user.id, 'status': status}
            }
        )

    async def user_status(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'user': event['message']['user'],
            'status': event['message']['status']
        }))
