import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import Message, CustomUser

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            self.room_group_name = "chat_room"
            await self.update_user_status(True)

            # Join room
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.update_user_status(False)
            # Leave room
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action', 'send_message')
        
        if action == 'send_message':
            message = data['message']
            receiver_id = data.get('receiver_id')

            if self.user.is_authenticated and receiver_id:
                # Save message to database
                msg_obj = await self.save_message(self.user, receiver_id, message)
                
                now = timezone.localtime(timezone.now()).strftime("%H:%M")

                # Send to group
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message_id': msg_obj.id,
                        'message': message,
                        'sender_id': self.user.id,
                        'receiver_id': int(receiver_id),
                        'user': self.user.username,
                        'timestamp': now
                    }
                )
        
        elif action == 'delete_message':
            message_id = data.get('message_id')
            if await self.delete_message(message_id):
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'message_deleted',
                        'message_id': message_id
                    }
                )

    @database_sync_to_async
    def save_message(self, sender, receiver_id, message):
        receiver = CustomUser.objects.get(id=receiver_id)
        return Message.objects.create(sender=sender, receiver=receiver, message=message)

    @database_sync_to_async
    def delete_message(self, message_id):
        try:
            msg = Message.objects.get(id=message_id, sender=self.user)
            msg.is_deleted = True
            msg.save()
            return True
        except Message.DoesNotExist:
            return False

    @database_sync_to_async
    def update_user_status(self, is_online):
        user = CustomUser.objects.get(id=self.user.id)
        user.is_online = is_online
        if not is_online:
            user.last_seen = timezone.now()
        user.save()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message_id': event['message_id'],
            'message': event['message'],
            'sender_id': event['sender_id'],
            'receiver_id': event['receiver_id'],
            'user': event['user'],
            'timestamp': event['timestamp']
        }))

    async def message_deleted(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message_deleted',
            'message_id': event['message_id']
        }))