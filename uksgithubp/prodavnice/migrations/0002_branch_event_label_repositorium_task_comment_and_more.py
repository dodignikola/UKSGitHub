# Generated by Django 4.2.4 on 2023-08-27 02:18

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prodavnice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('parent_branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prodavnice.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(default=datetime.datetime(2023, 8, 27, 4, 18, 49, 883306))),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Repositorium',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=160)),
                ('licence', models.CharField(max_length=20)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'Public'), ('PRIVATE', 'Private')], default='PRIVATE', max_length=15)),
                ('link', models.CharField(max_length=50)),
                ('number_of_forked_project', models.DecimalField(decimal_places=0, max_digits=5, null=True)),
                ('developers', models.ManyToManyField(blank=True, related_name='developers', to=settings.AUTH_USER_MODEL)),
                ('fork_parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prodavnice.repositorium')),
                ('lead', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('starred', models.ManyToManyField(related_name='starred', to=settings.AUTH_USER_MODEL)),
                ('watched', models.ManyToManyField(related_name='watched', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('date_created', models.DateTimeField(default=datetime.datetime(2023, 8, 27, 4, 18, 49, 883306))),
                ('asignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_to', to=settings.AUTH_USER_MODEL)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL)),
                ('labels', models.ManyToManyField(to='prodavnice.label')),
                ('repo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prodavnice.repositorium')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='prodavnice.event')),
                ('content', models.CharField(max_length=20)),
            ],
            bases=('prodavnice.event',),
        ),
        migrations.CreateModel(
            name='UpdateEvent',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='prodavnice.event')),
                ('field_name', models.CharField(max_length=20)),
                ('old_content', models.CharField(max_length=100)),
                ('new_content', models.CharField(max_length=100)),
            ],
            bases=('prodavnice.event',),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_reded', models.BooleanField(default=False)),
                ('message', models.CharField(blank=True, max_length=50)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prodavnice.repositorium')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Milestone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ime', models.CharField(max_length=50)),
                ('status', models.BooleanField(verbose_name='Open')),
                ('precentage', models.FloatField()),
                ('startDate', models.DateTimeField(verbose_name=datetime.datetime(2023, 8, 27, 4, 18, 49, 884303))),
                ('dueDate', models.DateTimeField()),
                ('repo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='prodavnice.repositorium')),
            ],
        ),
        migrations.AddField(
            model_name='label',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prodavnice.repositorium'),
        ),
        migrations.AddField(
            model_name='event',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='events', related_query_name='event', to='prodavnice.task'),
        ),
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(default=datetime.datetime(2023, 8, 27, 4, 18, 49, 884303))),
                ('log_message', models.CharField(max_length=40)),
                ('hash', models.CharField(max_length=30)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('branches', models.ManyToManyField(default=None, related_name='branches', to='prodavnice.branch')),
                ('parents', models.ManyToManyField(blank=True, to='prodavnice.commit', verbose_name='Parent commits')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prodavnice.repositorium'),
        ),
        migrations.CreateModel(
            name='Reaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('LIKE', 'Like'), ('DISLIKE', 'Dislike'), ('SMILE', 'Smile'), ('HOORAY', 'Hooray'), ('CONFUSED', 'Confused'), ('HEART', 'Heart'), ('ROCKET', 'Rocket'), ('EYES', 'Eyes')], default='LIKE', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prodavnice.comment')),
            ],
        ),
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='prodavnice.task')),
                ('state', models.CharField(choices=[('OPEN', 'Open'), ('CLOSED', 'Closed'), ('MERGED', 'Merged')], default='OPEN', max_length=20)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='prodavnice.branch')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to='prodavnice.branch')),
            ],
            bases=('prodavnice.task',),
        ),
        migrations.CreateModel(
            name='LabelApplication',
            fields=[
                ('event_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='prodavnice.event')),
                ('applied_labels', models.ManyToManyField(to='prodavnice.label')),
            ],
            bases=('prodavnice.event',),
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('task_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='prodavnice.task')),
                ('is_open', models.BooleanField(default=True)),
                ('milestone', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='prodavnice.milestone')),
            ],
            bases=('prodavnice.task',),
        ),
    ]
