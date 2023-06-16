from django.shortcuts import render, redirect
from django.http import JsonResponse
from accounts.models import CustomUser, Interest
from django.contrib.auth.decorators import login_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib import messages

# Create your views here.
@login_required
def index(request):
    template_name = 'index.html'
    cu = CustomUser.objects.get(username=request.user.username)
    interests = cu.interests.all()
    cu.is_connected = False
    cu.is_online = False
    cu.save()
    userCount = CustomUser.objects.filter(is_online=True).exclude(id=cu.id)
    context = {
        'interests': interests,
        'usercount': len(userCount)
    }
    return render(request, template_name, context)

@login_required
def chat_room(request, chat_room):
    url = chat_room
    chat_room = chat_room.split('-')
    try:
        user1 = CustomUser.objects.get(username=chat_room[1])
        user2 = CustomUser.objects.get(username=chat_room[0])
        if request.user.id == user1.id:
            first_user = user2 
            second_user = user1 
        else:
            first_user = user1 
            second_user = user2

        messages.success(request, "Your are successfully connected to "+str(first_user.full_name))
    except CustomUser.DoesNotExist:
        messages.error(request, "Some thing went wrong! Refresh page and try later.")
        return redirect('index')

    user1Interests = first_user.interests.all()
    user2Interests = second_user.interests.all()

    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        "notification_group_test",
        {
            "type": "send_notification",
            "notification": url
        }
    )

    user1.is_connected = True
    user2.is_connected = True 
    
    user1.save()
    user2.save()

    context = {
        'user1': first_user,
        'user2': second_user,
        'user1Interests': user1Interests,
        'user2Interests': user2Interests
    }

    return render(request, "chat.html", context)


def temp(request):
    template_name = 'temp.html'
    return render(request, template_name)
