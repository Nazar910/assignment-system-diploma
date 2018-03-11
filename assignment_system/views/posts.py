from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotFound
from django.forms import ModelForm
from django import forms
from django.contrib.auth.decorators import login_required

from assignment_system.models import Post, TaskOwner


class PostForm(ModelForm):
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
        model = Post
        fields = [
            'title', 'description', 'attachment'
        ]


@login_required(login_url='/assignment_system/login')
def post_list(request):
    if request.method != 'GET':
        return HttpResponseNotFound('Not found!')
    posts = Post.objects.all()
    return render(
        request,
        'assignment_system/post/post_list.html',
        {'posts': posts}
    )


@login_required(login_url='/assignment_system/login')
def create_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save()
        user = request.user
        task_owner = TaskOwner.objects.get(email=user.email)
        post.task_owner = task_owner
        post.save()
        # consider redirecting to get_one or something
        return redirect('post_list')
    return render(
        request,
        'assignment_system/post/post_form.html',
        {'form': form}
    )
    # return HttpResponse('create')


@login_required(login_url='/assignment_system/login')
def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        # consider redirecting to get_one or something
        return redirect('post_list')
    return render(
        request,
        'assignment_system/post/post_form.html',
        {'form': form}
    )
    # return HttpResponse('update')


@login_required(login_url='/assignment_system/login')
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(
        request,
        'assignment_system/post/post_confirm_delete.html',
        {'object': post}
    )
    # return HttpResponse('delete')


@login_required(login_url='/assignment_system/login')
def show_post_template(request, id):
    post = get_object_or_404(Post, id=id)
    return render(
        request,
        'assignment_system/post/post_template.html',
        {
            'post': post,
            'created_at': post.created_at.strftime("%d.%m.%Y")
        }
    )
