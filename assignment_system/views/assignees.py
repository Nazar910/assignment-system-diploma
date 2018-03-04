from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound, HttpResponse
from django.forms import ModelForm

from assignment_system.models import Assignee


class AssigneeForm(ModelForm):
    class Meta:
        model = Assignee
        fields = ['name', 'last_name', 'email']


def assignee_list(request):
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')

    assignees = Assignee.objects.all()
    context = {
        'assignees': assignees
    }
    return render(
        request,
        'assignment_system/assignee/assignee_list.html',
        context
    )


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
