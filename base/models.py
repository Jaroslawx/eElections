from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class ElectionEvent(models.Model):
    id_election = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    eligible_voters = models.ManyToManyField(User, related_name='eligible_elections')

    class Meta:
        verbose_name_plural = "Election Events"

    def __str__(self):
        return f"{self.type} Election ({self.start_date} - {self.end_date})"

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be earlier than end date.")


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_election = models.ForeignKey(ElectionEvent, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Vote"

    def __str__(self):
        return f"{self.user.username} vote in {self.id_election.type} election."


class Candidate(models.Model):
    id_candidate = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    id_election = models.ForeignKey(ElectionEvent, on_delete=models.CASCADE)
    votes = models.IntegerField()

    class Meta:
        verbose_name_plural = "Candidates"

    def __str__(self):
        return f"{self.name} {self.surname}"


class Report(models.Model):
    id_report = models.AutoField(primary_key=True)
    id_election = models.ForeignKey(ElectionEvent, on_delete=models.CASCADE)
    csv_file = models.FileField(upload_to='reports/', default='default.csv')
    frequency = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "Reports"

    def __str__(self):
        return f"Report for {self.id_election.type}"
