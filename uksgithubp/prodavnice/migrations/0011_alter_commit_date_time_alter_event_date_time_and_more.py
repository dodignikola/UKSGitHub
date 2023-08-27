# Generated by Django 4.2.4 on 2023-08-27 08:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prodavnice', '0010_alter_commit_date_time_alter_event_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commit',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 27, 10, 43, 13, 352153)),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 27, 10, 43, 13, 351156)),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='startDate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 8, 27, 10, 43, 13, 351156)),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 27, 10, 43, 13, 350160)),
        ),
    ]
