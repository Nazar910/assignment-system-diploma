# Generated by Django 2.0.2 on 2018-05-06 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment_system', '0006_auto_20180506_1751'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignmentevent',
            name='event_type',
            field=models.CharField(choices=[('fn', 'ЗАКІНЧЕНО'), ('st', 'РОЗПОЧАТО')], default='st', max_length=6),
        ),
    ]
