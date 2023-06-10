from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth import login, logout

# user logout
def logout_user(request):
    logout(request)
    return redirect('index')

# user signup
def signup(request):
    template_name = 'signup.html'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    
    context = {
            'form': form
        }
    return render(request, template_name, context)

# user login
def login_user(request):
    template_name = 'login.html'
    form = ''

    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index') 
    else:
        form = CustomLoginForm()
    context = {
            'form': form
        }
    return render(request, template_name, context)
