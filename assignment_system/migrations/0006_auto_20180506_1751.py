# Generated by Django 2.0.2 on 2018-05-06 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_system', '0005_auto_20180506_1741'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_type', models.CharField(choices=[('finished', 'ЗАКІНЧЕНО'), ('started', 'РОЗПОЧАТО')], default='started', max_length=6)),
                ('date', models.DateTimeField()),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment_system.Assignee', verbose_name='Виконувач')),
            ],
        ),
        migrations.RemoveField(
            model_name='assignmentfinished',
            name='assignee',
        ),
        migrations.RemoveField(
            model_name='assignmentfinished',
            name='assignment',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='finished_at',
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='started_at',
        ),
        migrations.DeleteModel(
            name='AssignmentFinished',
        ),
        migrations.AddField(
            model_name='assignmentevent',
            name='assignment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment_system.Assignment', verbose_name='Доручення'),
        ),
    ]