from django.db import models
from .taskowner import TaskOwner


class Post(models.Model):
    title = models.CharField('Заголовок', max_length=50)
    description = models.TextField('Опис')
    created_at = models.DateTimeField(auto_now_add=True)

    attachment = models.FileField(blank=True, null=True)

    task_owner = models.ForeignKey(
        TaskOwner,
        on_delete=models.CASCADE,
        # shitty
        blank=True,
        null=True
    )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.__str__()
