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
        ),
        # path(
        #         'assignments/assignee/<int:assignee_id>',
        #         views.get_assignments_by_assignee_id,
        #         name='get_assignments_by_assignee_id'
        # )
]

assignments_finished_urlpatterns = [
        path('assignments_finished', views.assignments_finished_list, name='assignments_finished_list')
]

urlpatterns = [
        path('', views.index, name='index'),
        path('home', views.home, name='home'),
        path('assignees/<int:id>', views.update_user_role, name='update_user_role'),
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
] + assignee_urlpatterns \
 + assignment_urlpatterns \
 + assignments_finished_urlpatterns
