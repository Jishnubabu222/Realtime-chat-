import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Message, CustomUser

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_group_name = "chat_room"

        # Join room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from browser
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        receiver_id = data.get('receiver_id')
        user = self.scope["user"]

        if user.is_authenticated and receiver_id:
            # Save message to database
            await self.save_message(user, receiver_id, message)

            now = timezone.now().strftime("%H:%M")

            # Send to group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'user': user.username,
                    'timestamp': now
                }
            )

    @database_sync_to_async
    def save_message(self, sender, receiver_id, message):
        try:
            receiver = CustomUser.objects.get(id=receiver_id)
            Message.objects.create(sender=sender, receiver=receiver, message=message)
        except CustomUser.DoesNotExist:
            pass

    # Receive message from room
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
            'timestamp': event.get('timestamp', '')
        }))