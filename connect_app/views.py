from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import CustomUser, Interest
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.
@login_required
def index(request):
    template_name = 'index.html'
    cu = CustomUser.objects.get(username=request.user.username)
    interests = cu.interests.all()
    userCount = CustomUser.objects.all().exclude(id=cu.id)
    context = {
        'interests': interests,
        'usercount': len(userCount)
    }
    return render(request, template_name, context)


@login_required
def chat_room(request, chat_room):
    url = chat_room
    chat_room = chat_room.split('-')
    user1 = chat_room[0]
    user2 = chat_room[1]

    user1 = CustomUser.objects.get(username=user2)
    user2 = CustomUser.objects.get(id=request.user.id)

    user1Interests = user1.interests.all()
    user2Interests = user2.interests.all()

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "notification_group_test",
        {
            "type": "send_notification",
            "notification": url
        }
    )

    context = {
        'user1': user1,
        'user2': user2,
        'user1Interests': user1Interests,
        'user2Interests': user2Interests
    }

    return render(request, "chat.html", context)


def temp(request):
    template_name = 'temp.html'
    return render(request, template_name)
