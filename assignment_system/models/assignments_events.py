from django.db import models
from .assignee import Assignee
from .assignment import Assignment


class AssignmentEvent(models.Model):
    FINISHED = 'fn'
    STARTED = 'st'

    __event_types = (
        (FINISHED, 'ЗАКІНЧЕНО'),
        (STARTED, 'РОЗПОЧАТО'),
    )

    event_type = models.CharField(
        max_length=6,
        choices=__event_types,
        default=STARTED
    )
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
    date = models.DateTimeField()

    def __str__(self):
        return self.assignment.__str__()

    def __unicode__(self):
        return self.__str__()
