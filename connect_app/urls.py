from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='index'),
    path('temp/', views.temp, name='temp'),
 
    path("chat/<str:user1>/", views.chat_room, name="chat_room"),
     
]
