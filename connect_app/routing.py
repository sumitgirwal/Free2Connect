from django.urls import re_path
from connect_app import consumers

websocket_urlpatterns = [
    re_path('ws/online_status/', consumers.OnlineStatusConsumer.as_asgi()),
]