from django.db import models
from .assignee import Assignee


class Assignment(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    assignees = models.ManyToManyField(Assignee)
    "Priority level"
    LOW_PRIORITY = 'l'
    MEDIUM_PRIORITY = 'm'
    HIGH_PRIORITY = 'h'
    UGRENT_PRIORITY = 'u'
    PRIORITIES = (
        (LOW_PRIORITY, 'Low'),
        (MEDIUM_PRIORITY, 'Medium'),
        (HIGH_PRIORITY, 'High'),
        (UGRENT_PRIORITY, 'Urgent')
    )
    priority_level = models.CharField(
        max_length=6,
        choices=PRIORITIES,
        default=LOW_PRIORITY
    )
    "Date stuff"
    assigned_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField()
