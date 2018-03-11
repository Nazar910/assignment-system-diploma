from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.forms import ModelForm
from django import forms
from django.contrib.auth.decorators import login_required

from assignment_system.models import Assignment, TaskOwner


class AssignmentForm(ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control'
            }
        )
    )
    assigned_at = forms.DateTimeField(
        widget=forms.SplitDateTimeWidget(),
        label="Назначено"
    )
    started_at = forms.DateTimeField(
        widget=forms.SplitDateTimeWidget(),
        label="Розпочато"
    )
    finished_at = forms.DateTimeField(
        widget=forms.SplitDateTimeWidget(),
        label="Закінчено"
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
    assignments = Assignment.objects.all()
    return render(
        request,
        'assignment_system/assignment/assignment_list.html',
        {'assignments': assignments}
    )


@login_required(login_url='/assignment_system/login')
def create_assignment(request):
    form = AssignmentForm(request.POST or None)
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
    user = request.user
    task_owner = get_object_or_404(TaskOwner, email=user.email)
    return render(
        request,
        'assignment_system/assignment/assignment_template.html',
        {
            'assignment': assignment,
            'created_at': assignment.created_at.strftime("%d.%m.%Y"),
            'assignees': assignees,
            'position': task_owner.position
        }
    )
