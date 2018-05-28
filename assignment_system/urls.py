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
        ),
        path(
                'assignees/assignment/<int:assignment_id>',
                views.get_assignees_by_assignment_id,
                name='get_assignees_by_assignment_id'
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
                'assignments/<int:id>',
                views.get_assignment_by_id,
                name='get_assignment_by_id'
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
        path('assignments_finished', views.assignments_finished_list, name='assignments_finished_list'),
        path(
                'assignments_finished/assignment/<int:id>',
                views.assignment_finished_by_assignment_id,
                name='assignment_finished_by_assignment_id'
        )
]

assignments_started_urlpatterns = [
        path('assignments_started', views.assignments_started_list, name='assignments_started_list'),
        path(
                'assignments_started/assignment/<int:id>',
                views.assignment_started_by_assignment_id,
                name='assignment_started_by_assignment_id'
        )
]

messages_urlpatterns = [
        path('messages/new', views.create_message, name='create_message'),
        path('messages/assignment/<int:id>', views.get_messages_by_assigmnent_id, name='get_messages_by_assignment_id'),
]

files_urlpatterns = [
        path('files/<int:message_id>', views.download_file, name='download_file'),       
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
 + assignments_finished_urlpatterns \
 + assignments_started_urlpatterns \
 + messages_urlpatterns \
 + files_urlpatterns
