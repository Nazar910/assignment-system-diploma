from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse

from assignment_system.models import Assignee


def assignees_list(request):
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')

    assignees = Assignee.objects.all()
    context = {
        'assignees': assignees
    }
    return render(
        request,
        'assignment_system/assignee/assignees_list.html',
        context
    )


def getOne(request, id):
    # return render(
    #     request,
    #     'assignment_system/assignee/getOne.html'
    # )
    return HttpResponse('getOne' + str(id))


def create(request):
    return HttpResponse('create')


def update(request):
    return HttpResponse('update')


def delete(request):
    return HttpResponse('delete')


def assignee(request, id):
    print('Id is ' + str(id))
    methods = {
        'GET': getOne,
        'POST': create,
        'PUT': update,
        'DELETE': delete
    }
    return methods[request.method](request, id)
