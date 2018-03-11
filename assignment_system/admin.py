from django.contrib import admin

# Register your models here.
from .models import Assignee, Assignment, TaskOwner

admin.site.register(Assignee)
admin.site.register(Assignment)
admin.site.register(TaskOwner)
