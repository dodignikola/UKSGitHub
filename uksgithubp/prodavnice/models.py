from django.db import models
from django.contrib.auth.models import User
import datetime
from django.urls import reverse

class ReactionType(models.TextChoices):
    Like = 'LIKE'
    Dislike = 'DISLIKE'
    Smile = 'SMILE'
    Hooray = 'HOORAY'
    Confused = 'CONFUSED'
    Heart = 'HEART'
    Rocket = 'ROCKET'
    Eyes = 'EYES'

class State(models.TextChoices):
    OPEN = 'OPEN'
    CLOSED = 'CLOSED'
    MERGED = 'MERGED'

class Visibility(models.TextChoices):
    PUBLIC = 'PUBLIC'
    PRIVATE = 'PRIVATE'

class Repositorium(models.Model):
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=160)
    licence = models.CharField(max_length=20)
    visibility = models.CharField(max_length=15, choices=Visibility.choices, default=Visibility.PRIVATE)
    link = models.CharField(max_length=50)
    lead = models.ForeignKey(User, on_delete=models.CASCADE)
    developers = models.ManyToManyField(to=User, blank=True, related_name="developers")
    starred = models.ManyToManyField(User, blank=True,related_name="starred")
    watched = models.ManyToManyField(User, blank=True,related_name="watched")
    #forked = models.ManyToManyField(, related_name="watched") zeza nesto...
    #number_of_forked_project = models.DecimalField(max_digits=5, null=True, blank=True,decimal_places=0)

    def __str__(self):
        return "%s/%s" % (self.lead, self.title)

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'pk': self.pk})

class Label(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Repositorium, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('label_detail', kwargs={'pk': self.pk})



class Task(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    date_created = models.DateTimeField(default=datetime.datetime.now())
    repo = models.ForeignKey(Repositorium, null=True, on_delete=models.CASCADE)
    asignee = models.ForeignKey(User, blank=True, null=True, related_name='assigned_to', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, blank=False, related_name='creator', on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label, blank=True)


class Event(models.Model):
    date_time = models.DateTimeField(default=datetime.datetime.now())
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="events", related_query_name="event")
    author = models.ForeignKey(User, blank=False, null=True, related_name='author', on_delete=models.CASCADE)



class LabelApplication(Event):
    applied_labels = models.ManyToManyField(Label)
    def __str__(self):
        label_names = [label.name for label in self.applied_labels.all()]
        if len(self.applied_labels.all()) > 0:
            return "%s applied labels %s at %s" % (self.author, label_names, str(self.date_time)[:-16])
        else:
            return "%s cleared all labels at %s"% (self.author, str(self.date_time)[:-16])



class Comment(Event):
    content = models.CharField(max_length=20)


class Milestone(models.Model):
    ime = models.CharField(max_length=50)
    status = models.BooleanField('Open')
    precentage = models.FloatField()
    startDate = models.DateTimeField(datetime.datetime.now())
    dueDate = models.DateTimeField()
    repo = models.ForeignKey(Repositorium,on_delete=models.CASCADE)

    def __str__(self):
        return self.ime
class Branch(models.Model):
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Repositorium, on_delete=models.CASCADE)
    parent_branch = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

    def get_absolute_url(self):
        return '/branches/'+self.pk

    def __str__(self):
        return "%s" % (self.name)


class Commit(models.Model):
    date_time = models.DateTimeField(default=datetime.datetime.now())
    log_message = models.CharField(max_length=40)
    hash = models.CharField(max_length=30)
    author = models.ForeignKey(User, blank=False, on_delete=models.CASCADE)
    branches = models.ManyToManyField(Branch, related_name='branches', blank=False, default=None)

    parents = models.ManyToManyField("self", symmetrical=False, blank=True, verbose_name=('Parent commits'))

    def get_absolute_url(self):
        return '/commits/'+self.pk

    def __str__(self):
        return "%s" % (self.hash[0:7])


class UpdateEvent(Event):
    field_name = models.CharField(max_length=20)
    old_content = models.CharField(max_length=100)
    new_content = models.CharField(max_length=100)

    def __str__(self):
        if self.field_name == 'is_open':
            if self.new_content.lower() == 'true':
                return "%s opened this issue at %s" % (self.author, str(self.date_time)[:-16])
            elif self.new_content.lower() == 'false':
                return "%s closed this issue at %s" % (self.author, str(self.date_time)[:-16])

        return "%s updated %s from %s to %s at %s" % (
        self.author, self.field_name, self.old_content, self.new_content, str(self.date_time)[:-16])


class Issue(Task):
    milestone = models.ForeignKey(Milestone, blank=True, null=True, on_delete=models.CASCADE)  # ManyToOne
    is_open = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('issue_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return "#%s - %s" % (self.id, self.title)


class PullRequest(Task):
    target = models.ForeignKey(Branch, blank=False, related_name='target', on_delete=models.CASCADE)
    source = models.ForeignKey(Branch, blank=False, related_name='source', on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=State.choices, default=State.OPEN)

    def get_absolute_url(self):
        return reverse('pull_request_detail', kwargs={'pk': self.pk})

class Reaction(models.Model):
    type = models.CharField(max_length=20, choices=ReactionType.choices, default=ReactionType.Like)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

class Notification(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, unique=False)  # OneToOne
    project = models.ForeignKey(Repositorium, null=True, on_delete=models.CASCADE)
    is_reded = models.BooleanField(default=False)
    message = models.CharField(max_length=50, unique=False, blank=True)


