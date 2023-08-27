from django.apps.registry import apps
from django.shortcuts import render, get_object_or_404, redirect



def pullreq(request):
    title=apps.get_app_config('prodavnice').verbose_name
    return render(request,"issues.html",{"title":title})
