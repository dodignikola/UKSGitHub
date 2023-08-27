from django.apps.registry import apps
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import PermissionDenied
from django.http import Http404

from .util import convert_to_boolean


# samo neki ovo mogu da vide
# za vise informacija pogledati https://docs.djangoproject.com/en/3.2/topics/auth/default/#the-permission-required-decorator
# 403 kod greske, ali se dozvoljava eventualno logovanje.
# podrazumevana putanja za logovanje je promenjena parametrom login_url

def login(request):
    # ukoliko je korisnik autentifikovan, proslediti ga na listu sa kasama
    if request.user.is_authenticated:
        return redirect('lista_kasa')
    title = apps.get_app_config('prodavnice').verbose_name
    if request.method == 'GET':
        return render(request, "kase_login.html", {"title": title})
    elif request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['psw']
        # pokusavamo autentifikaciju
        user = authenticate(request, username=username, password=password)
        if user:
            # uspesno
            login(request, user)
            # redirekcija na listu sa kasama, gde cemo proveriti permisije
            return redirect('index')
        else:
            # neuspesno
            return render(request, "kase_login.html", {"title": title, 'greska_login': True})
    else:
        raise Http404()


# https://www.delftstack.com/howto/django/django-check-logged-in-user/
def logout(request):
    # The user must be authenticated to do this.
    if request.user.is_authenticated:
        logout(request)
        return redirect('index')
    raise PermissionDenied()
