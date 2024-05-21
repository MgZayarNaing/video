# yourappname/consumers.py

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class UserStatusConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("user_status", self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("user_status", self.channel_name)

    def user_status(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']
        }))

class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)("notifications", self.channel_name)

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("notifications", self.channel_name)

    def send_notification(self, event):
        self.send(text_data=json.dumps({
            'message': event['message']
        }))
