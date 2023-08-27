# Generated by Django 4.2.4 on 2023-08-27 09:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prodavnice', '0013_alter_commit_date_time_alter_event_date_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commit',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 27, 11, 56, 17, 397963)),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 27, 11, 56, 17, 396965)),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='repo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prodavnice.repositorium'),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='startDate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 8, 27, 11, 56, 17, 396965)),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 27, 11, 56, 17, 395969)),
        ),
    ]