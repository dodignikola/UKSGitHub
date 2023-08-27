from django.apps.registry import apps
from django.shortcuts import render, get_object_or_404, redirect
from django.apps.registry import apps
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import Http404
from .models import Branch, Repositorium


def branches(request):
    title=apps.get_app_config('prodavnice').verbose_name
    branches=Branch.objects.all()
    return render(request,"branches.html",{"title":title,"branches":branches})

@login_required(login_url='/login')
def novagrana(request, id=None):
    title = apps.get_app_config('prodavnice').verbose_name
    if request.method == 'GET':
        repo = Repositorium.objects.all()
        branc = Branch.objects.all()
        return render(request, "novagrana.html", {"repo":repo, "parent":branc})
    else:
        greska_ime = None
        greska_prodavnica = None
        ime = request.POST['title']
        repo = request.POST['repo']
        parent = None
        try:
            parent = Branch.objects.get(pk=request.POST['parent'])
        except Exception:
            pass
        repos = Repositorium.objects.get(pk=repo)

        if title is not None and title == "":
            greska_ime = "Morate uneti Naziv"
        if repo is not None and repo == "":
            greska_prodavnica = "Morate uneti Opis"
        if greska_ime is None and greska_prodavnica is None and parent is not None:
            br = Branch(name = ime , project = repos, parent_branch = parent)
            br.save()
        else:
            br = Branch(name=ime, project=repos)
            br.save()
        return redirect('novagrana')

def brisiGrane(request, id):
    r = get_object_or_404(Branch, id=id)
    r.delete()
    return redirect('branches')