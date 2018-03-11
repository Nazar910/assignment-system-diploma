from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

assignee_urlpatterns = [
        path('assignees', views.assignee_list, name='assignee_list'),
        path('assignees/new', views.create_assignee, name='assignee_new'),
        path(
                'assignees/edit/<int:id>',
                views.update_assignee,
                name='assignee_edit'
        ),
        path(
                'assignees/delete/<int:id>',
                views.delete_assignee,
                name='assignee_delete'
        )
]

assignment_urlpatterns = [
        path('assignments', views.assignment_list, name='assignment_list'),
        path('assignments/new', views.create_assignment, name='assignment_new'),
        path(
                'assignments/edit/<int:id>',
                views.update_assignment,
                name='assignment_edit'
        ),
        path(
                'assignments/template/<int:id>',
                views.show_assignment_template,
                name='assignment_template'
        ),
        path(
                'assignments/delete/<int:id>',
                views.delete_assignment,
                name='assignment_delete'
        )
]

post_urlpatterns = [
        path('posts', views.post_list, name='post_list'),
        path('posts/new', views.create_post, name='post_new'),
        path(
                'posts/edit/<int:id>',
                views.update_post,
                name='post_edit'
        ),
        path(
                'posts/template/<int:id>',
                views.show_post_template,
                name='post_template'
        ),
        path(
                'posts/delete/<int:id>',
                views.delete_post,
                name='post_delete'
        )
]

directive_urlpatterns = [
        path('directives', views.directive_list, name='directive_list'),
        path('directives/new', views.create_directive, name='directive_new'),
        path(
                'directives/edit/<int:id>',
                views.update_directive,
                name='directive_edit'
        ),
        path(
                'directives/template/<int:id>',
                views.show_directive_template,
                name='directive_template'
        ),
        path(
                'directives/delete/<int:id>',
                views.delete_directive,
                name='directive_delete'
        )
]

urlpatterns = [
        path('', views.index, name='index'),
        path('home', views.home, name='home'),
        # Auth routes
        path('signup', views.signUp, name='signup'),
        # suggest logout for logged in users
        path(
                'login',
                auth_views.login,
                {'template_name': 'assignment_system/login.html'},
                name='login'
        ),
        path(
                'logout',
                auth_views.logout,
                {'template_name': 'assignment_system/logout.html'},
                name='logout'
        )
] + assignee_urlpatterns + assignment_urlpatterns + post_urlpatterns + directive_urlpatterns
