# Generated by Django 4.2.4 on 2023-08-27 07:56

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prodavnice', '0004_remove_repositorium_number_of_forked_project_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='reaction',
            name='issue',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='prodavnice.issue'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='commit',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 27, 9, 56, 35, 951710)),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 27, 9, 56, 35, 950714)),
        ),
        migrations.AlterField(
            model_name='milestone',
            name='startDate',
            field=models.DateTimeField(verbose_name=datetime.datetime(2023, 8, 27, 9, 56, 35, 951710)),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 27, 9, 56, 35, 949717)),
        ),
    ]
