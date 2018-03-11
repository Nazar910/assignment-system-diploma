from django.db import models


class TaskOwner(models.Model):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    patronymic = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return self.name + ' ' + self.last_name

    def __unicode__(self):
        return self.__str__()
