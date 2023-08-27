import datetime

from django.apps.registry import apps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import Http404

from .util import convert_to_boolean
from .models import Repositorium, Visibility, Issue, Task, Milestone

def milestones(request):
    title = apps.get_app_config('prodavnice').verbose_name
    miles = Milestone.objects.all()
    repo = Repositorium.objects.all()
    return render(request, "milestones.html", {"title": title, "milestones": miles, })


@login_required(login_url='/login')
def nmilestone(request, id=None):
    title = apps.get_app_config('prodavnice').verbose_name
    if request.method == 'GET':
        mile = Milestone.objects.all()
        repo = Repositorium.objects.all()
        return render(request, "unosmile.html", {"repo":repo})
    else:
        greska_ime = None
        greska_prodavnica = None
        ime = request.POST['title']
        repo = request.POST['repo']

        repos = Repositorium.objects.get(pk=repo)

        if title is not None and title == "":
            greska_ime = "Morate uneti Naziv"
        if repo is not None and repo == "":
            greska_prodavnica = "Morate uneti Opis"
        if greska_ime is None and greska_prodavnica is None:
            m = Milestone(ime = ime , status=True, precentage=0, startDate= datetime.datetime.now(), dueDate = datetime.datetime.now(), repo = repos )
            m.save()
        return redirect('nmilestone')

def obrisiMile(request, id):
    r=get_object_or_404(Milestone,id=id)
    r.delete()
    return redirect('milestones')