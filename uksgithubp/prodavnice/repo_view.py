from django.apps.registry import apps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import Http404

from .util import convert_to_boolean
from .models import Repositorium, Visibility, Issue, Task, Branch

from django.contrib.auth.models import User

def listaRepozitorijuma(request):
    title=apps.get_app_config('prodavnice').verbose_name
    repos=Repositorium.objects.all()
    return render(request,"listaRepo.html",{"title":title,"repos":repos})

def repo(request, id):
    title = apps.get_app_config('prodavnice').verbose_name
    issues = Issue.objects.filter(repo = id)
    task = Task.objects.filter(repo = id)
    repo = Repositorium.objects.get(id=id)
    return render(request, "repo.html", {"repo":repo, "title": title, "issues": issues,"tasks": task})

def opcijeRepo(request, id):
    title = apps.get_app_config('prodavnice').verbose_name
    users = User.objects.all()
    issues = Issue.objects.filter(repo = id)
    branc = Branch.objects.filter(project = id)
    repos = Repositorium.objects.get(id=id)
    user = repos.developers.all()


    return render(request, "opcijerepo.html", {"users":users,"branc":branc, "title": title, "repo":repos, "user":user})

@login_required(login_url='/login')
def promeniNazRepo(request, id=None):
    title = apps.get_app_config('prodavnice').verbose_name
    if request.method == 'GET':
        user = Repositorium.objects.filter(developers=id)
        issues = Issue.objects.filter(repo=id)
        task = Task.objects.filter(repo=id)
        branc = Branch.objects.filter(project=id)
        repos = Repositorium.objects.get(id=id)
        users = User.objects.all()
        return render(request, "opcijerepo.html", {"branc": branc, "title": title, "repo": repos, "user": user})

    else:
        greska_ime = None
        ime = request.POST['repo']

        if ime is not None and ime == "":
            greska_ime = "Morate uneti Naziv"

        if greska_ime is None:
            r = Repositorium.objects.get(id=id)
            r.title = ime
            r.save()
        return redirect('lista_repozitorijuma',)

@login_required(login_url='/login')
def novirepo(request, id=None):
    title = apps.get_app_config('prodavnice').verbose_name
    if request.method == 'GET':
        v = Visibility.values
        repos = Repositorium.objects.all()
        return render(request, "unosRepo.html")
    else:
        greska_ime = None
        greska_des = None
        greska_licenca = None
        ime = request.POST['title']
        des = request.POST['description']
        licenca = request.POST['licenca']
        public = request.POST['public']
        try:
            public, public_converted = convert_to_boolean(request.POST['public'])
        except:
            public = False

        if title is not None and title == "":
            greska_ime = "Morate uneti Naziv"
        if des is not None and des == "":
            greska_des = "Morate uneti Opis"
        if licenca is not None and licenca == "":
            greska_licenca = "Morate odrediti Licencu"

        if greska_ime is None and greska_des is None and greska_licenca is None:
            r = Repositorium(title=ime, description=des, licence=licenca, visibility=Visibility.PUBLIC if public == True else Visibility.PRIVATE, link=title+request.user.username, lead=request.user)
            r.save()
        return redirect('lista_repozitorijuma')

def obrisirepo(request, id):
    r=get_object_or_404(Repositorium,id=id)
    r.delete()
    return redirect('lista_repozitorijuma')