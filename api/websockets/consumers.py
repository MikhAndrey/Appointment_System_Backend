import json

from channels.generic.websocket import AsyncWebsocketConsumer


class AppointmentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('appointment_notifications', self.channel_name)
        await super().connect()

    async def appointment_delete(self, text_data=None):
        await self.send_json(text_data)

    async def appointment_create(self, text_data=None):
        await self.send_json(text_data)

    async def appointment_update(self, text_data=None):
        await self.send_json(text_data)

    async def send_json(self, text_data=None):
        await self.send(json.dumps(text_data))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('appointment_notifications', self.channel_name)
        await super().disconnect(close_code)
