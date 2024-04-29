from django.db import models
from django.contrib.auth.models import User


class Election(models.Model):
    id_election = models.AutoField(primary_key=True)
    type = models.CharField(max_length=20)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Election"

    def __str__(self):
        return f"{self.type} Election ({self.start_date} - {self.end_date})"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_election = models.ForeignKey(Election, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Vote"

    def __str__(self):
        return f"Vote for {self.id_election.type} by {self.user.username}"


class Candidate(models.Model):
    id_candidate = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    party_beliefs = models.CharField(max_length=100)
    # TODO: change name for sth more relevant (if i start for student mayor of the year it is no party_beliefs)

    id_election = models.ForeignKey(Election, on_delete=models.CASCADE)
    votes = models.IntegerField()

    class Meta:
        verbose_name_plural = "Candidates"

    def __str__(self):
        return f"{self.name} {self.surname}"


class Report(models.Model):
    id_report = models.AutoField(primary_key=True)
    id_election = models.ForeignKey(Election, on_delete=models.CASCADE)
    results = models.JSONField()
    frequency = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        verbose_name_plural = "Reports"

    def __str__(self):
        return f"Report for {self.id_election.type}"


# TODO: add sth like status for user, so we can check if user can vote here or not (like student, worker, etc)
