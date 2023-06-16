from django.urls import path
from connect_app import consumers

websocket_urlpatterns = [

    path('ws/online_status/', consumers.OnlineConnectConsumer.as_asgi()),
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
    path('ws/rooms/<room_name>/', consumers.ChatConsumer.as_asgi()),
    path('ws/online/', consumers.OnlineConsumer.as_asgi())
    
]