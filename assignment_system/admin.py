from django.contrib import admin

# Register your models here.
from .models import Assignee, Assignment

admin.site.register(Assignee)
admin.site.register(Assignment)
