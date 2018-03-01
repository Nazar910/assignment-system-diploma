from django.shortcuts import render


def index(request):
    return render(request, 'assignment_system/index.html')
