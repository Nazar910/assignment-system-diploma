from django.db import models
from .assignee import Assignee
from .assignment import Assignment


class AssignmentFinished(models.Model):
    assignee = models.ForeignKey(
        Assignee,
        verbose_name='Виконувач',
        on_delete=models.CASCADE
    )
    assignment = models.ForeignKey(
        Assignment,
        verbose_name='Доручення',
        on_delete=models.CASCADE
    )
    finished_at = models.DateTimeField()

    def __str__(self):
        return self.assignment.__str__()

    def __unicode__(self):
        return self.__str__()
