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

urlpatterns = [
        path('', views.index, name='index'),
        path('home', views.home, name='home'),
        path('assignments', views.assignments_list, name='assignments_list'),
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
] + assignee_urlpatterns
