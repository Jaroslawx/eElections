import os
import csv
from django.conf import settings
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q, Count


from .models import ElectionEvent, Candidate, Vote, Report
from django.contrib.auth.views import (LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from .forms import SignUpForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm


def home(request):
    return render(request, "home.html")


def all_elections(request):
    now = timezone.now()
    query = request.GET.get('q', '')

    # Filter and annotate elections with the number of candidates
    started_elections = ElectionEvent.objects.filter(start_date__lte=now, end_date__gte=now).annotate(
        candidate_count=Count('candidate'))
    no_started_elections = ElectionEvent.objects.filter(start_date__gt=now).annotate(candidate_count=Count('candidate'))
    ended_elections = ElectionEvent.objects.filter(end_date__lt=now).annotate(candidate_count=Count('candidate'))

    # If a search query is provided
    if query:
        # Filter elections by type
        started_elections = started_elections.filter(Q(type__icontains=query))
        no_started_elections = no_started_elections.filter(Q(type__icontains=query))
        ended_elections = ended_elections.filter(Q(type__icontains=query))

    user_voted_elections = []
    if request.user.is_authenticated:
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
    return render(request, "elections/results.html", {"election": election, "candidates": candidates})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_elections(request):
    elections = ElectionEvent.objects.all()
    election_data = []

    for election in elections:
        total_voters = election.eligible_voters.count()
        votes_cast = Vote.objects.filter(id_election=election).count()
        total_candidates = Candidate.objects.filter(id_election=election).count()
        election_data.append({
            'election': election,
            'total_voters': total_voters,
            'votes_cast': votes_cast,
            'total_candidates': total_candidates
        })

    if request.method == "POST":
        if 'end_election' in request.POST:
            election_id = request.POST['end_election']
            election = ElectionEvent.objects.get(id_election=election_id)
            election.end_date = timezone.now()
            election.save()
        elif 'generate_report' in request.POST:
            election_id = request.POST['generate_report']
            # Logic to generate report
            return generate_report(request, election_id)

    return render(request, "elections/admin_elections.html", {
        "election_data": election_data
    })


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


def generate_report(request, election_id):
    # Retrieve data needed for the report
    election = ElectionEvent.objects.get(id_election=election_id)
    total_voters = election.eligible_voters.count()
    votes_cast = Vote.objects.filter(id_election=election).count()

    # Retrieve candidates with their respective vote counts
    candidates = Candidate.objects.filter(id_election=election)
    candidates_votes = [(candidate.name + " " + candidate.surname, candidate.votes) for candidate in candidates]

    # Calculate turnout percentage
    if total_voters > 0:
        turnout_percentage = (votes_cast / total_voters) * 100
    else:
        turnout_percentage = 0

    # Create a path to the "reports" folder in the project
    reports_folder = os.path.join(settings.BASE_DIR, 'reports')

    # Create the folder if it doesn't exist
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)

    # Create the file name for the report
    file_name = f"election_report_{election_id}.csv"
    file_path = os.path.join(reports_folder, file_name)

    # Create the CSV file and save the report
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Type of Election', 'Turnout', 'Votes Cast'])
        writer.writerow([election.type, f'{turnout_percentage:.2f}%', votes_cast])
        writer.writerow([])
        writer.writerow(['Candidate', 'Votes'])
        for candidate, votes in candidates_votes:
            writer.writerow([candidate, votes])

    # Save information about the report in the database
    report_instance = Report.objects.create(id_election=election, csv_file=file_name, frequency=turnout_percentage)

    # Return the HTTP response with the CSV file
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'

    return response

