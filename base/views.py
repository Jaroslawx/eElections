from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q
import csv

from .models import ElectionEvent, Candidate, Vote, Report
from django.contrib.auth.views import (LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from django.contrib.auth.models import User
from .forms import SignUpForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm


def home(request):
    return render(request, "home.html")


@login_required
def all_elections(request):
    now = timezone.now()
    query = request.GET.get('q', '')

    # Filter elections
    started_elections = ElectionEvent.objects.filter(start_date__lte=now, end_date__gte=now)
    no_started_elections = ElectionEvent.objects.filter(start_date__gt=now)
    ended_elections = ElectionEvent.objects.filter(end_date__lt=now)

    # If a search query is provided
    if query:
        # Filter elections by type
        started_elections = started_elections.filter(Q(type__icontains=query))
        no_started_elections = no_started_elections.filter(Q(type__icontains=query))
        ended_elections = ended_elections.filter(Q(type__icontains=query))

    # Get votes for the current user
    user_votes = Vote.objects.filter(user=request.user)

    # Get IDs of elections user has voted in
    user_voted_elections = user_votes.values_list('id_election', flat=True)

    return render(request, "elections/all_elections.html", {
        "started_elections": started_elections,
        "no_started_elections": no_started_elections,
        "ended_elections": ended_elections,
        "query": query,
        "user_voted_elections": user_voted_elections
    })


def vote(request, election_id):
    if request.method == "POST":
        candidate_id = request.POST.get("candidate")
        candidate = Candidate.objects.get(pk=candidate_id)
        candidate.votes += 1  # We increase the number of votes for the selected candidate
        candidate.save()  # We save the changes in the database

        # Save that the user participated in this election
        user = request.user
        election = ElectionEvent.objects.get(pk=election_id)
        Vote.objects.create(user=user, id_election=election)

        return redirect("thank_you")  # Redirected to a thank_you page
    else:
        election = ElectionEvent.objects.get(pk=election_id)
        candidates = Candidate.objects.filter(id_election=election_id)
        return render(request, "elections/vote.html", {"election": election, "candidates": candidates})


def thank_you(request):
    return render(request, "elections/thank_you.html")


def election_results(request, election_id):
    election = get_object_or_404(ElectionEvent, pk=election_id)
    candidates = Candidate.objects.filter(id_election=election_id).order_by('-votes')
    return render(request, "elections/election_results.html", {"election": election, "candidates": candidates})


def admin_elections(request):
    elections = ElectionEvent.objects.all()
    election_data = []

    for election in elections:
        total_voters = election.eligible_voters.count()
        votes_cast = Vote.objects.filter(id_election=election).count()
        election_data.append({
            'election': election,
            'total_voters': total_voters,
            'votes_cast': votes_cast
        })

    if request.method == 'POST':
        if 'end_election' in request.POST:
            election_id = request.POST.get('end_election')
            election = get_object_or_404(ElectionEvent, id=election_id)
            election.end_date = timezone.now()
            election.save()
            messages.success(request, f"Election {election} has been ended early.")

        elif 'generate_report' in request.POST:
            election_id = request.POST.get('generate_report')
            return redirect('generate_report', election_id=election_id)

    context = {
        'election_data': election_data
    }
    return render(request, 'admin_elections.html', context)


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user to the database
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # New user authentication
            user = authenticate(username=username, password=password)
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('home')


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy('home')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'registration/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_reset_complete.html'
