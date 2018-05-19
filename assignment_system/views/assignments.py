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
    accept = request.META['HTTP_ACCEPT']
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')

    assignment = get_object_or_404(Assignment, id=id)
    serialized = serializers.serialize('json', [assignment])

    if accept == 'application/json':
        return HttpResponse(serialized)

    if 'text/html' in accept:
        return render(
            request,
            'assignment_system/assignment/assignment_editor.html',
            {
                'assignment': serialized,
                'priorities': json.dumps(dict((y, x) for x, y in Assignment.PRIORITIES))
            }
        )

    return HttpResponseNotFound('Not found!')


@login_required(login_url='/assignment_system/login')
def assignment_list(request):
    accept = request.META['HTTP_ACCEPT']
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')

    if accept == 'application/json':
        user = request.user
        assignee = get_object_or_404(Assignee, email=user.email)
        assignments = get_list_or_404(Assignment, author_id=assignee.id)

        return HttpResponse(serializers.serialize('json', assignments))

    if 'text/html' in accept:
        return render(
            request,
            'assignment_system/assignment/assignment_list.html'
        )

    return HttpResponseNotFound('Not found!')


@login_required(login_url='/assignment_system/login')
def create_assignment(request):
    user = request.user
    assignee = Assignee.objects.get(email=user.email)
    if assignee.role == Assignee.JUST_ASSIGNEE:
        return HttpResponseForbidden('У вас немає доступу до створення доручень!')

    form = AssignmentForm(request.POST or None)
    print(form)
    if form.is_valid():
        assignment = form.save()
        task_owner = TaskOwner.objects.get(email=user.email)
        assignment.task_owner = task_owner
        assignment.save()
        # consider redirecting to get_one or something
        return redirect('assignment_list')
    return render(
        request,
        'assignment_system/assignment/assignment_form.html',
        {'form': form}
    )
    # return HttpResponse('create')


@login_required(login_url='/assignment_system/login')
def update_assignment(request, id):
    user = request.user
    assignee = Assignee.objects.get(email=user.email)

    assignment = get_object_or_404(Assignment, id=id)
    form = AssignmentForm(request.POST or None, instance=assignment)
    if form.is_valid():
        form.save()
        # consider redirecting to get_one or something
        return redirect('assignment_list')
    return render(
        request,
        'assignment_system/assignment/assignment_form.html',
        {
            'form': form,
            'just_assignee': assignee.role == Assignee.JUST_ASSIGNEE
        }
    )
    # return HttpResponse('update')


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
