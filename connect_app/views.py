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
    context = {
        'interests': interests
    }
    return render(request, template_name, context)

def chat_room(request, room_name):
    return render(request, "chat.html", {"room_name": room_name})
