from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.forms import ModelForm
from django import forms
from django.contrib.auth.decorators import login_required

from assignment_system.models import Directive, TaskOwner


class DirectiveForm(ModelForm):
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

    class Meta:
        model = Directive
        fields = [
            'title', 'description', 'attachment'
        ]


@login_required(login_url='/assignment_system/login')
def directive_list(request):
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')
    directives = Directive.objects.all()
    return render(
        request,
        'assignment_system/directive/directive_list.html',
        {'directives': directives}
    )


@login_required(login_url='/assignment_system/login')
def create_directive(request):
    form = DirectiveForm(request.POST or None)
    if form.is_valid():
        directive = form.save()
        user = request.user
        task_owner = TaskOwner.objects.get(email=user.email)
        directive.task_owner = task_owner
        directive.save()
        # consider redirecting to get_one or something
        return redirect('directive_list')
    return render(
        request,
        'assignment_system/directive/directive_form.html',
        {'form': form}
    )
    # return HttpResponse('create')


@login_required(login_url='/assignment_system/login')
def update_directive(request, id):
    directive = get_object_or_404(Directive, id=id)
    form = DirectiveForm(request.POST or None, instance=directive)
    if form.is_valid():
        form.save()
        # consider redirecting to get_one or something
        return redirect('directive_list')
    return render(
        request,
        'assignment_system/directive/directive_form.html',
        {'form': form}
    )
    # return HttpResponse('update')


@login_required(login_url='/assignment_system/login')
def delete_directive(request, id):
    directive = get_object_or_404(Directive, id=id)
    if request.method == 'POST':
        directive.delete()
        return redirect('directive_list')
    return render(
        request,
        'assignment_system/directive/directive_confirm_delete.html',
        {'object': directive}
    )
    # return HttpResponse('delete')


@login_required(login_url='/assignment_system/login')
def show_directive_template(request, id):
    directive = get_object_or_404(Directive, id=id)
    return render(
        request,
        'assignment_system/directive/directive_template.html',
        {
            'directive': directive,
            'created_at': directive.created_at.strftime("%d.%m.%Y")
        }
    )
