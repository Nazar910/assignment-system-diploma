from django.db import models


class AssignmentPriority(models.Model):
    "Priorities"
    LOW = 'l'
    MEDIUM = 'm'
    HIGH = 'h'
    UGRENT = 'u'
    PRIORITIES = (
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High'),
        (UGRENT, 'Urgent')
    )
    level = models.CharField(
        max_length=6,
        choices=PRIORITIES,
        default=LOW
    )
