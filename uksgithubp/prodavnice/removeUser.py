from django.apps.registry import apps
from django.shortcuts import render, get_object_or_404, redirect
from django.apps.registry import apps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import Http404
from .models import Branch, Repositorium

from .models import Repositorium, Visibility, Issue, Task, Branch

from django.contrib.auth.models import User

def removeUser(request, id):
    repos = Repositorium.objects.get(id=id)
    user = request.POST['users']
    if user is not None and user == "":
        greska_ime = "Morate uneti Naziv"

    if greska_ime is None:
        r = Repositorium.objects.get(id=id)
        r.developers.remove(user)
        r.save()
    return redirect('lista_repozitorijuma')

@login_required(login_url='/login')
def adduser(request, id=None):
    if request.method == 'GET':
        pass
    else:
        greska_ime = None
        user = request.POST['users']

        if user is not None and user == "":
            greska_ime = "Morate uneti Naziv"

        if greska_ime is None:
            r = Repositorium.objects.get(id=id)
            r.developers.add(user)
            r.save()
        return redirect('lista_repozitorijuma',)
