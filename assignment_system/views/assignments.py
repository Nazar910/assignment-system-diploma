from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.forms import ModelForm
from django import forms

from assignment_system.models import Assignment


class AssignmentForm(ModelForm):
    assigned_at = forms.DateTimeField(widget=forms.SelectDateWidget())
    started_at = forms.DateTimeField(widget=forms.SelectDateWidget())
    finished_at = forms.DateTimeField(widget=forms.SelectDateWidget())

    class Meta:
        model = Assignment
        fields = [
            'title', 'description', 'assignees',
            'priority_level', 'assigned_at',
            'started_at', 'finished_at'
        ]


def assignment_list(request):
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')
    assignments = Assignment.objects.all()
    return render(
        request,
        'assignment_system/assignment/assignment_list.html',
        {'assignments': assignments}
    )


def create_assignment(request):
    form = AssignmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        # consider redirecting to get_one or something
        return redirect('assignment_list')
    return render(
        request,
        'assignment_system/assignment/assignment_form.html',
        {'form': form}
    )
    # return HttpResponse('create')


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
