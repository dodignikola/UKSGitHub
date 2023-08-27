from django.apps.registry import apps
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import Http404

from django.contrib.auth.models import User
from .util import convert_to_boolean
from .models import Repositorium, Visibility, Issue, Milestone,Reaction, ReactionType, Comment

@login_required(login_url='/login')
def unosIssue(request, id=None):
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

def issues(request):
    title=apps.get_app_config('prodavnice').verbose_name
    issues=Issue.objects.all()
    return render(request,"issues.html",{"title":title,"issues":issues})

def issue(request, id):
    title=apps.get_app_config('prodavnice').verbose_name
    i=Issue.objects.get(id=id)
    return render(request,"listaissue.html",{"title":title,"issue":i})

def obrisiissue(request, id):
    i=get_object_or_404(Issue,id=id)
    i.delete()
    return redirect("lista_repozitorijuma")


def zatvori(request, id):
    i=Issue.objects.get(id=id)
    i.is_open=False
    i.save()
    return redirect("issues")
def otvori(request, id):
    i = Issue.objects.get(id=id)
    i.is_open = True
    i.save()
    return redirect("issues")