from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class ElectionEvent(models.Model):
    id_election = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20, verbose_name="Election Type",
                            help_text="Type of the election, e.g., Presidential, Parliamentary.")
    start_date = models.DateTimeField(verbose_name="Start Date",
                                      help_text="The date and time when the election starts.")
    end_date = models.DateTimeField(verbose_name="End Date", help_text="The date and time when the election ends.")
    eligible_voters = models.ManyToManyField(User, related_name='eligible_elections', verbose_name="Eligible Voters",
                                             help_text="Users eligible to vote in this election.")

    class Meta:
        verbose_name = "Election Event"
        verbose_name_plural = "Election Events"

    def __str__(self):
        return f"{self.type} Election ({self.start_date.strftime('%Y-%m-%d')} - {self.end_date.strftime('%Y-%m-%d')})"

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be earlier than end date.")


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Voter")
    id_election = models.ForeignKey(ElectionEvent, on_delete=models.CASCADE, verbose_name="Election")

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        constraints = [
            models.UniqueConstraint(fields=['user', 'id_election'], name='unique_vote')
        ]

    def __str__(self):
        return f"{self.user.username} vote in {self.id_election.type} election"


class Candidate(models.Model):
    id_candidate = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="First Name", help_text="First name of the candidate.")
    surname = models.CharField(max_length=100, verbose_name="Last Name", help_text="Last name of the candidate.")
    description = models.CharField(max_length=100, verbose_name="Description",
                                   help_text="Short description or slogan of the candidate.")
    id_election = models.ForeignKey(ElectionEvent, on_delete=models.CASCADE, verbose_name="Election")
    votes = models.PositiveIntegerField(default=0, verbose_name="Vote Count",
                                        help_text="Number of votes the candidate has received.")

    class Meta:
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"

    def __str__(self):
        return f"{self.name} {self.surname} ({self.id_election.type} Election)"


class Report(models.Model):
    id_report = models.AutoField(primary_key=True)
    id_election = models.ForeignKey(ElectionEvent, on_delete=models.CASCADE, verbose_name="Election")
    csv_file = models.FileField(upload_to='reports/', default='default.csv', verbose_name="CSV File",
                                help_text="CSV file containing the report.")
    frequency = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Frequency",
                                    help_text="Frequency of the report generation.")

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"

    def __str__(self):
        return f"Report for {self.id_election.type} election"
