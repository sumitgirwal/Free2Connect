from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync
from django.shortcuts import redirect
from accounts.models import CustomUser
from django.db.models import Q

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "online_users"
        self.room_group_name = f"online_users_group"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        print("Connecting.....")
        await self.accept()


    async def notify_connected(self, userId):
        notification = {
            'type': 'connected',
            'user_id': userId,
            'message': 'You are now connected in the chat room.'
        }
        await self.send(text_data=json.dumps(notification))
    
    async def disconnect(self, close_code):
        print("Disconnecting.....")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        user = await self.get_user()
        if user is not None:
            await self.set_user_offline(user)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_offline',
                    'user_id': user.id
                }
            )
    

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        if data['status'] == 'online':
            user = await self.get_user()
            if user is not None:
                await self.set_user_online(user)
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'user_online',
                        'user_id': user.id
                    }
                )
        elif data['status'] == 'connect':
            user = await self.get_user()
            if user is not None:
                connected_user_id = data['user_id']
                connected_user = await self.get_user_by_id(connected_user_id)
                if connected_user is not None and connected_user.is_online:
                    random_user = await self.get_connected_users_with_same_interest(connected_user)
                    if random_user:
                      
                        # Send the message to the room group
                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'chat_message',
                                'message': "Working received the chat invite"
                            }
                        )

                        await self.send(text_data=json.dumps(random_user))

    async def chat_message(self, event):
        message = event['message']
        typeM = event['type']

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'type': typeM,
            'message': message
        }))

    @database_sync_to_async      
    def get_connected_users_with_same_interest(self, current_user ):
        current_user_interests = current_user.interests.all() 
        random_user = CustomUser.objects.exclude(
            Q(id=current_user.id) & Q(is_connected=True)
        ).filter(
            is_online=True,
            interests__in=current_user_interests
        ).order_by('?').first() 
        random_user.is_connected = True
        random_user.save()
        return [random_user.id, random_user.username]
    
                     


    async def user_online(self, event):
        user_id = event['user_id']

        # Send a message to the WebSocket
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'status': 'online'
        }))

    async def user_offline(self, event):
        user_id = event['user_id']

        # Send a message to the WebSocket
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'status': 'offline'
        }))

    @database_sync_to_async
    def get_user(self):
        return self.scope['user']

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        return CustomUser.objects.filter(id=user_id).first()

    @database_sync_to_async
    def set_user_online(self, user):
        user.is_online = True
        user.save()

    @database_sync_to_async
    def set_user_offline(self, user):
        user.is_online = False
        user.save()


# Chat Consumer
# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

#         # Add the user to the chat room group
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Remove the user from the chat room group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         # Handle received messages
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'message': text_data
#             }
#         )

#     async def chat_message(self, event):
#         # Send the received message to all users in the chat room
#         message = event['message']
#         await self.send(text_data=message)
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))