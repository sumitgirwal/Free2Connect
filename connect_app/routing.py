from django.urls import re_path, path
from connect_app import consumers

websocket_urlpatterns = [

    re_path('ws/online_status/', consumers.OnlineConsumer.as_asgi()),
    re_path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
    path('ws/rooms/<room_name>/', consumers.ChatConsumer.as_asgi())
    
]