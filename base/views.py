from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Election, Candidate, Vote, Report


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
