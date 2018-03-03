from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm


@login_required(login_url='/assignment_system/login')
def home(request):
    return render(request, 'assignment_system/home.html')


def index(request):
    return render(request, 'assignment_system/index.html')


# todo: ugly
def signUp(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            savedUser = form.save()
            username = savedUser.username
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'assignment_system/signup.html', {'form': form})
