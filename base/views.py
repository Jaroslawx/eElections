from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils import timezone

from .models import Election, Candidate, Vote, Report


def signup(request):
    if request.method == "POST":
        # Pobieranie danych z formularza rejestracji
        username = request.POST['username']
        password = request.POST['password']
        # Tworzenie nowego użytkownika
        User.objects.create_user(username=username, password=password)
        # Logowanie nowego użytkownika
        user = authenticate(username=username, password=password)
        auth_login(request, user)
        return redirect('home')
    else:
        return render(request, "accounts/signup.html")


# TODO: zamienic na klase?
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            # Logowanie użytkownika
            auth_login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, "accounts/login.html", {'form': form})


def home(request):
    return render(request, "home.html")


def all_elections(request):
    # TODO: change to all elections available for that user, or add filters to see specific group of elections
    today = timezone.now().date()
    started_elections = Election.objects.filter(start_date__lte=today)
    no_started_elections = Election.objects.filter(start_date__gt=today)
    return render(request, "all_elections.html",
                  {"started_elections": started_elections, "no_started_elections": no_started_elections})


def vote(request, election_id):
    if request.method == "POST":
        candidate_id = request.POST.get("candidate")
        candidate = Candidate.objects.get(pk=candidate_id)
        candidate.votes += 1  # We increase the number of votes for the selected candidate
        candidate.save()  # We save the changes in the database
        return redirect("thank_you")  # Redirected to a thank_you page
    else:
        election = Election.objects.get(pk=election_id)
        candidates = Candidate.objects.filter(id_election=election_id)
        return render(request, "vote.html", {"election": election, "candidates": candidates})


def thank_you(request):
    return render(request, "thank_you.html")
