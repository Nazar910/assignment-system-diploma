from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.forms import ModelForm
from django import forms
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from datetime import datetime

from assignment_system.models import Assignment, TaskOwner, Assignee


class AssignmentForm(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Заголовок'
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Опис'
    )
    assigned_at = forms.DateTimeField(
        widget=forms.DateTimeInput(),
        label="Назначено",
        initial=datetime.now()
    )
    started_at = forms.DateTimeField(
        widget=forms.DateTimeInput(),
        label="Розпочато",
        initial=datetime.now()
    )
    finished_at = forms.DateTimeField(
        widget=forms.DateTimeInput(),
        label="Закінчено",
        initial=datetime.now()
    )
    attachment = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={
                'multiple': True
            }
        ),
        label="Вкладення",
        required=False
    )
    priority_level = forms.CharField(
        widget=forms.Select(choices=Assignment.PRIORITIES),
        label='Пріорітет'
    )

    class Meta:
        model = Assignment
        fields = [
            'title', 'description', 'assignees',
            'priority_level', 'assigned_at',
            'started_at', 'finished_at', 'attachment'
        ]


@login_required(login_url='/assignment_system/login')
def assignment_list(request):
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')
    user = request.user
    task_owner = TaskOwner.objects.get(email=user.email)
    assignee = Assignee.objects.get(email=user.email)
    assignments_assigned_to_me = None
    if assignee:
        assignments_assigned_to_me = assignee.assignment_set \
            .all() \
            .exclude(task_owner=task_owner)

    assignments_created_by_me = Assignment.objects \
        .filter(task_owner=task_owner)
    return render(
        request,
        'assignment_system/assignment/assignment_list.html',
        {
            'assignments_created_by_me': assignments_created_by_me,
            'assignments_assigned_to_me': assignments_assigned_to_me
        }
    )


@login_required(login_url='/assignment_system/login')
def create_assignment(request):
    form = AssignmentForm(request.POST or None)
    print(form)
    if form.is_valid():
        assignment = form.save()
        user = request.user
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
    assignment = get_object_or_404(Assignment, id=id)
    form = AssignmentForm(request.POST or None, instance=assignment)
    if form.is_valid():
        form.save()
        # consider redirecting to get_one or something
        return redirect('assignment_list')
    return render(
        request,
        'assignment_system/assignment/assignment_form.html',
        {'form': form}
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
