from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from assignment_system.forms import SignUpForm
from assignment_system.models import Assignment, TaskOwner


@login_required(login_url='/assignment_system/login')
def home(request):
    user = request.user
    task_owner = TaskOwner.objects.get(email=user.email)
    return render(
        request,
        'assignment_system/home.html',
        {
            'first_name': user.first_name,
            'patronymic': task_owner.patronymic,
            'username': user.username
        })


def update_user_role(request, id):
    # TODO add auth
    print('Id', id)
    print('POST', request.body)
    return HttpResponse('Hi')


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
