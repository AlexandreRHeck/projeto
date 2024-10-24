# clinic/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class PasswordConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'password_updates'

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_password_update(self, event):
        data = event['data']
        
        # Send message to WebSocket
        await self.send(text_data=json.dumps(data))
