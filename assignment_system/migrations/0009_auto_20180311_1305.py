# Generated by Django 2.0.2 on 2018-03-11 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_system', '0008_auto_20180311_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignee',
            name='last_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='assignee',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='assignee',
            name='patronymic',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
