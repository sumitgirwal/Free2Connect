# from channels.generic.websocket import WebsocketConsumer
# import json

# class OnlineStatusConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         if data['status'] == 'online':
#             # Code to handle user being online
#             print(data)
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from asgiref.sync import async_to_sync

class OnlineStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "online_users"
        self.room_group_name = f"online_users_group"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
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
        else:
            # complete the offline 
            pass 
        
    async def user_online(self, event):
        user_id = event['user_id']

        # Send a message to the WebSocket
        await self.send(text_data=json.dumps({
            'user_id': user_id,
            'status': 'online'
        }))

    @database_sync_to_async
    def get_user(self):
        return self.scope['user']

    @database_sync_to_async
    def set_user_online(self, user):
        user.is_online = True
        user.save()
