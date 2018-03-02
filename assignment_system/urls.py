from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
        path('', views.index, name='index'),
        path('home', views.home, name='home'),
        path('signup', views.signUp, name='signup'),
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
]
