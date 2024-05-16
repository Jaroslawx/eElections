from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse_lazy
import csv

from .models import ElectionEvent, Candidate, Vote, Report
from django.contrib.auth.views import (LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,
                                       PasswordResetCompleteView)
from .forms import SignUpForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm


def home(request):
    return render(request, "home.html")


def all_elections(request):
    # TODO: change to all elections available for that user, or add filters to see specific group of elections
    today = timezone.now().date()
    started_elections = ElectionEvent.objects.filter(start_date__lte=today)
    no_started_elections = ElectionEvent.objects.filter(start_date__gt=today)
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
        election = ElectionEvent.objects.get(pk=election_id)
        candidates = Candidate.objects.filter(id_election=election_id)
        return render(request, "vote.html", {"election": election, "candidates": candidates})


def thank_you(request):
    return render(request, "thank_you.html")


def create_report(request):
    if request.method == 'POST':
        # Retrieving data for a report from a POST request

        # Saving data to a CSV file
        with open('reports/report.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            # Here we save the data to a CSV file

        # Creating a report object in the database
        report = Report.objects.create(
            id_election=request.POST['id_election'],
            frequency=request.POST['frequency'],
        )
        report.csv_file.save('report.csv', open('reports/report.csv', 'rb'))

        return render(request, 'success.html', {'message': 'Report created successfully'})
    else:
        # Displaying the form for creating a report
        return render(request, 'create_report.html')


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
    return render(request, "accounts/signup.html", {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('home')


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm

    def get_success_url(self):
        return reverse_lazy('home')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    template_name = 'accounts/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'
