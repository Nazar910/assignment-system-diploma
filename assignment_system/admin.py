from django.contrib import admin

# Register your models here.
from .models import Assignee, Assignment, AssignmentEvent, Message

admin.site.register(Assignee)
admin.site.register(Assignment)
admin.site.register(AssignmentEvent)
admin.site.register(Message)
