from django.db import models
from .assignee import Assignee


class Assignment(models.Model):
    author = models.ForeignKey(
        Assignee,
        on_delete=models.CASCADE,
        # shitty
        blank=True,
        null=True,
        related_name='%(class)s_which_created_assignee'
    )
    title = models.CharField('Заголовок', max_length=50)
    description = models.TextField('Опис')
    assignees = models.ManyToManyField(Assignee, verbose_name='Виконувачі')
    "Priority level"
    LOW_PRIORITY = 'l'
    MEDIUM_PRIORITY = 'm'
    HIGH_PRIORITY = 'h'
    UGRENT_PRIORITY = 'u'
    PRIORITIES = (
        (LOW_PRIORITY, 'НИЗЬКИЙ'),
        (MEDIUM_PRIORITY, 'СЕРЕДНІЙ'),
        (HIGH_PRIORITY, 'ВИСОКИЙ'),
        (UGRENT_PRIORITY, 'ТЕРМІНОВО')
    )
    priority_level = models.CharField(
        max_length=6,
        choices=PRIORITIES,
        default=LOW_PRIORITY
    )
    "Date stuff"
    assigned_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(blank=True, null=True)

    attachment = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()
