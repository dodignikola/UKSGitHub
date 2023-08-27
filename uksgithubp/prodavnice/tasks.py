from django.apps.registry import apps
from django.db import models
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import Http404

from django.contrib.auth.models import User
from .util import convert_to_boolean
from .models import Repositorium, Visibility,Event, Task, Milestone,Reaction, ReactionType, Comment

@login_required(login_url='/login')
def dodajTask(request, id=None):
    title = apps.get_app_config('prodavnice').verbose_name
    repo = Repositorium.objects.all()
    users = User.objects.all()
    mile = Milestone.objects.all()
    if request.method == 'GET':
        return render(request, "unosIssue.html", {"repo": repo, "users": users, "milestone":mile})
    else:
        greska_naziv = None
        greska_opis = None
        greska_repo = None
        greska_ass = None
        greska_mile = None
        naziv = request.POST['title']
        des = request.POST['description']
        repo = request.POST['repo']
        ass = request.POST['users']
        mile = request.POST['milestone']

        repos = Repositorium.objects.get(pk=repo)
        userAss = User.objects.get(pk=ass)

        if naziv is not None and naziv == "":
            greska_naziv = "Morate uneti Naziv"
        if des is not None and des == "":
            greska_opis = "Morate uneti Opis"
        if repo is not None and repo == "":
            greska_repo = "Morate odrediti Repo"
        if ass is not None and ass == "":
            greska_ass = "Morate odrediti Assignea"
        if mile is not None and mile == "":
            greska_mile = "Morate odrediti Milestone"

        if greska_naziv is None and greska_opis is None and greska_repo is None and greska_ass is None and greska_mile is None:
            i = Issue(title=naziv, description=des, repo=repos, asignee=userAss, creator=request.user, milestone=Milestone.objects.get(pk=mile), is_open = True)
            i.save()
        return redirect('unosIssue')

def task(request, id):
    title=apps.get_app_config('prodavnice').verbose_name
    task=Task.objects.get(id=id)
    return render(request,"task.html",{"title":title,"task":task})

def obrisitask(request, id):
    i=get_object_or_404(Task,id=id)
    i.delete()
    return redirect("lista_repozitorijuma")

def kom(request, id):
    if request.method == 'POST':
        emoji = request.POST['emoji']
        comm = request.POST['comm']
        emo = None
        if emoji == 'LIKE':
            emo = ReactionType.Like
        elif emoji == 'DISLIKE':
            emo = ReactionType.Dislike
        elif emoji == 'SMILE':
            emo = ReactionType.Smile
        elif emoji == 'HOORAY':
            emo = ReactionType.Hooray
        elif emoji == 'CONFUSED':
            emo = ReactionType.Confused
        elif emoji == 'HEART':
            emo = ReactionType.Heart
        elif emoji == 'ROCKET':
            emo = ReactionType.Rocket
        elif emoji == 'EYES':
            emo = ReactionType.Eyes
        e=Event.save(date_time = datetime.datetime.now(), task=Task.object.get(pk=id), author=request.user)
        c= Comment.save(comm)
        r = Reaction.save(type = emo, user=request.user, comment=c)
        return redirect("lista_repozitorijuma")
    else:
        title = apps.get_app_config('prodavnice').verbose_name
        task = Task.objects.get(id=id)
        r = Reaction.objects.all()
        return render(request, "task.html", {"title": title, "task": task, "r":r})


