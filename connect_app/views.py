from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def index(request):
    template_name = 'index.html'
    context = {}
    return render(request, template_name, context)

def update_state(request):
    if request.method == 'POST' and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        new_state = request.POST.get('state')
        new_state = True if new_state.lower() == 'offline' else False
        user = request.user
        user.is_online = new_state
        user.save()
        response = {'state': new_state}
        return JsonResponse(response)
    return JsonResponse({'error': 'Invalid request'})
