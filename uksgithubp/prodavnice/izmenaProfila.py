from django.apps.registry import apps
from django.shortcuts import render, get_object_or_404, redirect

from .util import convert_to_float, convert_to_boolean
from django.contrib.auth.models import User



def brisanjeProfila(request):
    for a in User.objects.all():
        if a == request.user:
            a.delete()
    return redirect('index')


def izmenaProfila(request):
    if request.method == 'GET':
        title=apps.get_app_config('prodavnice').verbose_name
        password = request.user.password
        email = request.user.email
        return render(request, "izmenaProfila.html", {"email":email, "password":password, "password2":password})
    else:
        user = User
        greska_ = False
        for a in User.objects.all():
            if a.username == request.POST['user'] and a.username != request.user.username:
                greska_ = True
            if a.email == request.POST['email'] and a.email != request.user.email:
                greska = True
            if a == request.user:
                user = a
        if not greska_:
            user.username = request.POST['user']
            user.email = request.POST['email']
            user.save()
        return redirect('izmenaProfila')

def registracija(request):
    if request.method == 'GET':
        return render(request, "registracija.html", )
    else:
        usernameOznaka = None
        emailOznaka = None
        passwordOznaka = None
        password2Oznaka = None

        username = request.POST['userime']
        email = request.POST['emailic']
        password = request.POST['password']
        password2 = request.POST['password2']

        if username is not None and username =="":
            usernameOznaka="Morate uneti Username"
        if email is not None and email =="":
            emailOznaka="Morate uneti Email"
        if password is not None and len(password) < 8:
            passwordOznaka="Morate uneti Password od minimum 8 karaktera"
        if password2 is not None and len(password2) < 8:
            password2Oznaka="Morate uneti Password od minimum 8 karaktera"
        if password is not None and password2 is not None and len(password2) > 8 and password2 != password:
            passwordOznaka="Morate uneti isti Password"
            password2Oznaka = "Morate uneti isti Password"
        if usernameOznaka is None and emailOznaka is None and passwordOznaka is None:
            greska_ = False
            for a in User.objects.all():
                if a.username == request.POST['userime'] and a.username != request.user.username:
                    greska_ = True
                if a.email == request.POST['emailic'] and a.email != request.user.email:
                    greska = True
                if a == request.user:
                    user = a
            if not greska_:
                User.objects.create_user(username, email, password)
        return redirect('register')

