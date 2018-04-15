from django.contrib import admin

# Register your models here.
from .models import Assignee, Assignment, TaskOwner, Post, Directive, AssignmentFinished

admin.site.register(Assignee)
admin.site.register(Assignment)
admin.site.register(TaskOwner)
admin.site.register(Post)
admin.site.register(Directive)
admin.site.register(AssignmentFinished)
