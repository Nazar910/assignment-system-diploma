from django.shortcuts import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello world, it is assignment_system app")
