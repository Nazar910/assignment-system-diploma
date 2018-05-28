from django.db import models
from .assignment import Assignment, Assignee


class Message(models.Model):
    author = models.ForeignKey(
        Assignee,
        on_delete=models.CASCADE,
        # shitty
        blank=True,
        null=True,
        related_name='%(class)s_which_created_assignee'
    )
    text = models.TextField('Текст')
    author_full_name = models.TextField('Текст')
    assignment = models.ForeignKey(
        Assignment,
        verbose_name='Автор',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(null=True, upload_to='media')

    def __str__(self):
        return self.text

    def __unicode__(self):
        return self.__str__()
