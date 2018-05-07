# Generated by Django 2.0.2 on 2018-05-06 14:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_system', '0004_assignment_deadline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='directive',
            name='task_owner',
        ),
        migrations.RemoveField(
            model_name='post',
            name='task_owner',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='task_owner',
        ),
        migrations.AddField(
            model_name='assignment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignment_which_created_assignee', to='assignment_system.Assignee'),
        ),
        migrations.DeleteModel(
            name='Directive',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='TaskOwner',
        ),
    ]