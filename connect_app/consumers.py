import json
from django.db.models import Q
from asgiref.sync import async_to_sync
from django.shortcuts import redirect
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from accounts.models import CustomUser
from connect_app.models import Room, Message


# Online Consumer
class OnlineConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "online_users"
        self.room_group_name = f"online_users_group"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
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
                    url = connected_user.username+'-'+random_user[1]
                    if random_user:

                        await self.send(text_data=json.dumps({'user_type': 'receiver', 'random_user': random_user, 'url': url}))

                        await self.channel_layer.group_send(
                            self.room_group_name,
                            {
                                'type': 'chat_message',
                                'message': "Working received the chat invite",
                                'random_user': random_user,
                                'url': url,
                                'senderID': random_user[0],
                                'receiverID': connected_user.id
                            }
                        )

    async def chat_message(self, event):
        typeM = event['type']
        message = event['message']
        random_user = event['random_user']
        url = event['url']
        senderID = event['senderID']
        receiverID = event['receiverID']

        await self.send(text_data=json.dumps({
            'senderID': senderID,
            'receiverID': receiverID,
            'type': typeM,
            'message': message,
            'random_user': random_user,
            'url': url

        }))

    @database_sync_to_async
    def get_connected_users_with_same_interest(self, current_user):
        current_user_interests = current_user.interests.all()
        # trying to match the interest
        random_user = CustomUser.objects.exclude(
            Q(id=current_user.id) & Q(is_connected=True)
        ).filter(
            is_online=True,
            interests__in=current_user_interests
        ).order_by('?').first()

        # if not matching to any interest
        if random_user == None:
            random_user = CustomUser.objects.exclude(
                Q(id=current_user.id) & Q(is_connected=True)
            ).filter(
                is_online=True
            ).order_by('?').first()
            
        random_user.is_connected = True
        random_user.save()
        return [random_user.id, random_user.username]

    async def user_online(self, event):
        user_id = event['user_id']
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'status': 'online'
        }))

    async def user_offline(self, event):
        user_id = event['user_id']
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


# Notification Consumer
class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = f'notification_group_test'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.loads(text_data)

    async def send_notification(self, event):
        notification = event['notification']
        await self.send(text_data=json.dumps(notification))

# Chat consumer
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        print(self.room_name)
        self.room_group_name = 'chat_%s' % self.room_name

        # # Join room group
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
        user_id = text_data_json['user_id']
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user_id': user_id,
                'message': message
            }
        )
        

    async def chat_message(self, event):
        user_id = event['user_id']
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'message': message

        }))
        