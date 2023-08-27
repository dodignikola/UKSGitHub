from django.apps.registry import apps
from django.shortcuts import render, get_list_or_404



def index(request):
    title = apps.get_app_config('prodavnice').verbose_name
    return render(request, 'index.html', {"title": title})