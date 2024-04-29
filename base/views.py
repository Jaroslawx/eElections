from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Election, Candidate, Vote, Report


def home(request):
    return render(request, "home.html")


def all_elections(request):
    elections = Election.objects.all()  # We retrieve all selections from the database
    return render(request, "all_elections.html", {"all_elections": elections})


def vote(request, election_id):
    if request.method == "POST":
        candidate_id = request.POST.get("candidate")
        candidate = Candidate.objects.get(pk=candidate_id)
        candidate.votes += 1  # We increase the number of votes for the selected candidate
        candidate.save()  # We save the changes in the database
        return redirect("thank_you")  # Redirected to a thank you page
    else:
        election = Election.objects.get(pk=election_id)
        candidates = Candidate.objects.filter(id_election=election_id)
        return render(request, "vote.html", {"election": election, "candidates": candidates})


def thank_you(request):
    return render(request, "thank_you.html")
