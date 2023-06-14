from django.shortcuts import render
from django.http import JsonResponse
from accounts.models import CustomUser, Interest
from django.contrib.auth.decorators import login_required

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
def chat_room(request, user1):
    user1 = CustomUser.objects.get(id=user1)
    user2 = CustomUser.objects.get(id=request.user.id)

    user1Interests =  user1.interests.all()
    user2Interests =  user2.interests.all()
    
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