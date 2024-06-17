# eElections/base/tests/test_models.py
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User
from base.models import ElectionEvent, Vote, Candidate, Report
from django.utils import timezone
from datetime import datetime, timedelta


class ElectionEventModelTest(TestCase):
    def setUp(self):
        self.election_event = ElectionEvent.objects.create(
            type='Presidential',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1)
        )

    def test_election_event_creation(self):
        self.assertTrue(isinstance(self.election_event, ElectionEvent))
        self.assertEqual(self.election_event.__str__(), f"{self.election_event.type} Election ({self.election_event.start_date.strftime('%Y-%m-%d')} - {self.election_event.end_date.strftime('%Y-%m-%d')})")

    def test_election_event_date_validation(self):
        with self.assertRaises(ValidationError):
            election_event_invalid = ElectionEvent(
                type='Parliamentary',
                start_date=timezone.now(),
                end_date=timezone.now() - timedelta(days=1)
            )
            election_event_invalid.clean()


class VoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.election_event = ElectionEvent.objects.create(
            type='Presidential',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1)
        )
        self.vote = Vote.objects.create(user=self.user, id_election=self.election_event)

    def test_vote_creation(self):
        self.assertTrue(isinstance(self.vote, Vote))
        self.assertEqual(self.vote.__str__(), f"{self.user.username} vote in {self.election_event.type} election")

    def test_vote_unique_constraint(self):
        with self.assertRaises(Exception):
            duplicate_vote = Vote.objects.create(user=self.user, id_election=self.election_event)


class CandidateModelTest(TestCase):
    def setUp(self):
        self.election_event = ElectionEvent.objects.create(
            type='Presidential',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=1)
        )
        self.candidate = Candidate.objects.create(
            name='John',
            surname='Doe',
            description='A candidate',
            id_election=self.election_event,
            votes=0
        )

    def test_candidate_creation(self):
        self.assertTrue(isinstance(self.candidate, Candidate))
        self.assertEqual(self.candidate.__str__(), f"{self.candidate.name} {self.candidate.surname} ({self.candidate.id_election.type} Election)")

    def test_candidate_add_vote(self):
        initial_votes = self.candidate.votes
        self.candidate.add_vote()
        self.assertEqual(self.candidate.votes, initial_votes + 1)


# class ReportModelTest(TestCase):
#     def setUp(self):
#         self.election_event = ElectionEvent.objects.create(
#             type='Presidential',
#             start_date=timezone.now(),
#             end_date=timezone.now() + timedelta(days=1)
#         )
#         self.report = Report.objects.create(
#             id_election=self.election_event,
#             frequency=75.00
#         )
#
#     def test_report_creation(self):
#         self.assertTrue(isinstance(self.report, Report))
#         self.assertEqual(self.report.__str__(), f"Report for {self.report.id_election.type} election")
#
#     def test_report_csv_file_name(self):
#         self.report.save()
#         self.assertTrue(self.report.csv_file.name.endswith(f'report_{self.report.id_election.id_election}.csv'))
