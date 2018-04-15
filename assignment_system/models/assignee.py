from django.db import models


class Assignee(models.Model):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30, blank=True)
    email = models.EmailField()

    SUPERVISOR = 'sv'
    SECRETARY = 'sc'
    JUST_ASSIGNEE = 'ja'

    __roles = (
        (SUPERVISOR, 'КЕРІВНИК'),
        (SECRETARY, 'СЕКРЕТАР'),
        (JUST_ASSIGNEE, 'ВИКОНУВАЧ')
    )

    role = models.CharField(
        max_length=6,
        choices=__roles,
        default=JUST_ASSIGNEE
    )

    position = models.TextField(default='викладач')

    def __str__(self):
        return self.name + ' ' + self.last_name

    def __unicode__(self):
        return self.__str__()
