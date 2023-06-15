from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomLoginForm
from django.contrib.auth import login, logout
from django.contrib import messages

# user logout
def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out Successfully.")
    return redirect('index')

# user signup
def signup(request):
    template_name = 'signup.html'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Successfully Signup. Please login now.")
            return redirect('login')
        else:
            messages.error(request, "Something went wrong! Check your signup information.")
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
            messages.success(request, "Your Successfully Loggedin.")
            login(request, user)
            return redirect('index') 
        else:
            messages.error(request, "Something went wrong! Check your signup information.")
    else:
        form = CustomLoginForm()
    context = {
            'form': form
        }
    return render(request, template_name, context)
