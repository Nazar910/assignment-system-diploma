from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponseNotFound, HttpResponse, HttpResponseForbidden
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime
from django.core import serializers

from assignment_system.models import Assignment, Assignee

import json


def filter_by_assignee(assignee_id):
    return Assignee.objects.filter(assignee_id=assignee_id)


@login_required(login_url='/assignment_system/login')
def get_assignments_by_assignee_id(request, assignee_id):
    assignments = filter_by_assignee(assignee_id)

    return HttpResponse(serializers.serialize('json', assignments))


@login_required(login_url='/assignment_system/login')
def get_assignment_by_id(request, id):
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')

    assignment = get_object_or_404(Assignment, id=id)
    serialized = serializers.serialize('json', [assignment])
    assignees_serialized = serializers.serialize('json', Assignee.objects.all())
    selected_assignees_serialized = serializers.serialize('json', assignment.assignees.all())

    accept = request.META['HTTP_ACCEPT']
    if accept == 'application/json':
        return HttpResponse(serialized)

    if 'text/html' in accept:
        return render(
            request,
            'assignment_system/assignment/assignment_editor.html',
            {
                'assignment': serialized,
                'assignees': assignees_serialized,
                'selected_assignees': selected_assignees_serialized,
                'priorities': json.dumps(dict((y, x) for x, y in Assignment.PRIORITIES))
            }
        )

    return HttpResponseNotFound('Not found!')


@login_required(login_url='/assignment_system/login')
def assignment_list(request):
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')

    accept = request.META['HTTP_ACCEPT']
    if accept == 'application/json':
        user = request.user
        assignee = get_object_or_404(Assignee, email=user.email)
        # assignments = get_list_or_404(Assignment, author_id=assignee.id)
        assignments = Assignment.objects.all()

        return HttpResponse(serializers.serialize('json', assignments))

    if 'text/html' in accept:
        return render(
            request,
            'assignment_system/assignment/assignment_list.html'
        )

    return HttpResponseNotFound('Not found!')


@login_required(login_url='/assignment_system/login')
def create_assignment(request):
    if request.method != 'POST':
        return HttpResponseNotFound('Not found')

    user = request.user
    assignee = Assignee.objects.get(email=user.email)
    if assignee.role == Assignee.JUST_ASSIGNEE:
        return HttpResponseForbidden('У вас немає доступу до створення доручень!')

    accept = request.META['HTTP_ACCEPT']
    if 'text/html' in accept:
        return render(
            request,
            'assignment_system/assignment/assignment_editor.html',
            {
                'is_new': 'true'
            }
        )

    print('Request body is', json.loads(request.body))
    return HttpResponseNotFound('Not found!')


@login_required(login_url='/assignment_system/login')
def update_assignment(request, id):
    if request.method != 'POST':
        return HttpResponseNotFound('Not found')

    user = request.user
    assignee = Assignee.objects.get(email=user.email)
    if assignee.role == Assignee.JUST_ASSIGNEE:
        return HttpResponseForbidden('У вас немає доступу до створення доручень!')

    print('This is update')
    print('Request body is', json.loads(request.body))
    data = json.loads(request.body)
    assignment = get_object_or_404(Assignment, id=id)
    assignment.title = data['title']
    assignment.description = data['description']
    print('Priority before', assignment.priority_level)
    print('Priority data["priority"]', data['priority'])
    assignment.priority_level = data['priority']
    print('Priority after', assignment.priority_level)

    if data['deadline'] != '':
        assignment.deadline = data['deadline']

    assignment.assignees.clear()
    for assignee_id in data['assignees']:
        assignee = get_object_or_404(Assignee, id=assignee_id)
        assignment.assignees.add(assignee)

    assignment.save()
    return HttpResponse('update')


@login_required(login_url='/assignment_system/login')
def delete_assignment(request, id):
    assignment = get_object_or_404(Assignment, id=id)
    if request.method == 'POST':
        assignment.delete()
        return redirect('assignment_list')
    return render(
        request,
        'assignment_system/assignment/assignment_confirm_delete.html',
        {'object': assignment}
    )
    # return HttpResponse('delete')


@login_required(login_url='/assignment_system/login')
def show_assignment_template(request, id):
    assignment = get_object_or_404(Assignment, id=id)
    assignees = assignment.assignees.all()
    return render(
        request,
        'assignment_system/assignment/assignment_template.html',
        {
            'assignment': assignment,
            'created_at': assignment.created_at.strftime("%d.%m.%Y"),
            'assignees': assignees,
            'position': assignment.task_owner.position
        }
    )
