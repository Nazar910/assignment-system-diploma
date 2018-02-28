from django.db import models
from .assignee import Assignee
from .assignment_priority import AssignmentPriority


# Create your models here.
class Assignment(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    assignees = models.ManyToManyField(Assignee)
    priority = models.ForeignKey(AssignmentPriority, on_delete=models.PROTECT)
    "Date stuff"
    assigned_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
