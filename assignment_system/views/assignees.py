from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.core import serializers

from assignment_system.models import Assignee, Assignment


class AssigneeForm(ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Ім\'я'
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        ),
        label='Прізвище'
    )
    email = forms.EmailField(
        max_length=254, help_text='Введіть коректну email-адресу.',
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
            }
        )
    )

    class Meta:
        model = Assignee
        fields = ['name', 'last_name', 'email']


@login_required(login_url='/assignment_system/login')
def assignee_list(request):
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')

    assignees = Assignee.objects.all()

    if request.META['HTTP_ACCEPT'] == 'application/json':
        return HttpResponse(serializers.serialize('json', assignees))

    context = {
        'assignees': assignees
    }
    return render(
        request,
        'assignment_system/assignee/assignee_list.html',
        context
    )


def get_assignees_by_assignment_id(request, assignment_id):
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')

    assignment = get_object_or_404(Assignment, id=assignment_id)

    assignees = assignment.assignees.all()

    return HttpResponse(serializers.serialize('json', assignees))


def get_one(request, id):
    # consider get from cache or pass somehow
    assignee = Assignee.objects.get(id=id)

    context = {
        'assignee': assignee
    }

    return render(
        request,
        'assignment_system/assignee/get_one.html',
        context
    )


@login_required(login_url='/assignment_system/login')
def create_assignee(request):
    form = AssigneeForm(request.POST or None)
    if form.is_valid():
        form.save()
        # consider redirecting to get_one or something
        return redirect('assignee_list')
    return render(
        request,
        'assignment_system/assignee/assignee_form.html',
        {'form': form}
    )
    # return HttpResponse('create')


@login_required(login_url='/assignment_system/login')
def update_assignee(request, id):
    assignee = get_object_or_404(Assignee, id=id)
    form = AssigneeForm(request.POST or None, instance=assignee)
    if form.is_valid():
        form.save()
        # consider redirecting to get_one or something
        return redirect('assignee_list')
    return render(
        request,
        'assignment_system/assignee/assignee_form.html',
        {'form': form}
    )
    # return HttpResponse('update')


@login_required(login_url='/assignment_system/login')
def delete_assignee(request, id):
    assignee = get_object_or_404(Assignee, id=id)
    if request.method == 'POST':
        assignee.delete()
        return redirect('assignee_list')
    return render(
        request,
        'assignment_system/assignee/assignee_confirm_delete.html',
        {'object': assignee}
    )
    # return HttpResponse('delete')
