from channels.generic.websocket import AsyncWebsocketConsumer

import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        group_name = str(self.scope['url_route']['kwargs']['user_id'])
        await self.channel_layer.group_add(group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard('notifications', self.channel_name)

    async def send_notification(self, event):
        notification = event['notification']

        await self.send(
            text_data=json.dumps(
                {
                    "notification": notification
                }
            )
        )
