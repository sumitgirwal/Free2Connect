from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def signup(request):
    template_name = 'signup.html'
    form = ''

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_auth:login')
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form
        }
    return render(request, template_name, context)