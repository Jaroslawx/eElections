from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def all_elections(request):
    return render(request, "all_elections.html", {"all_elections": all_elections})


def vote(request):
    return render(request, "vote.html")
